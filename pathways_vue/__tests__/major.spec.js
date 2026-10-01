import { flushPromises, mount } from "@vue/test-utils";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { createMemoryHistory, createRouter } from "vue-router";

vi.mock("@/composables/customFetch", () => ({ useCustomFetch: vi.fn() }));
vi.mock("@/utils.js", () => ({ default: { recentViewManager: vi.fn() } }));
// Stubs don't apply to defineAsyncComponent wrappers, so mock the modules
vi.mock("@/components/major/d3-cgpa.vue", () => ({ default: {} }));
vi.mock("@/components/major/similar-major.vue", () => ({ default: {} }));
vi.mock("@/components/major/common-courses.vue", () => ({ default: {} }));

import { useCustomFetch } from "@/composables/customFetch";
import Major from "@/pages/major.vue";

const mountAt = async (id) => {
  const router = createRouter({
    history: createMemoryHistory(),
    routes: [{ path: "/major", component: Major }],
  });
  router.push({ path: "/major", query: { id } });
  await router.isReady();
  const wrapper = mount(Major, {
    global: {
      plugins: [router],
      stubs: {
        DefaultLayout: { template: "<div><slot name='content' /></div>" },
        MajorDetails: true,
        ExploreMajor: true,
        D3Cgpa: true,
        SimilarMajor: true,
        CommonCourses: true,
        ContactAdviser: true,
        SearchMini: true,
      },
    },
  });
  await flushPromises();
  return { wrapper, router };
};

const match = (code, title) => ({
  credential_code: code,
  credential_title: title,
  major_campus: "Seattle",
  major_school: "Arts",
});

describe("Major page", () => {
  beforeEach(() => {
    vi.mocked(useCustomFetch).mockReset();
  });

  it("loads full major data for a credential code", async () => {
    vi.mocked(useCustomFetch).mockResolvedValue({
      credential_title: "Music",
      major_campus: "Seattle",
    });
    const { wrapper } = await mountAt("MUSAP-0-1-8");
    expect(useCustomFetch).toHaveBeenCalledWith(
      "/api/v1/majors/details/MUSAP-0-1-8",
    );
    expect(wrapper.vm.major_data.credential_title).toBe("Music");
  });

  it("lists links when a bare code has multiple matches", async () => {
    vi.mocked(useCustomFetch).mockResolvedValue({
      matches: [match("C SCI-0-1-1", "CS A"), match("C SCI-10-1-1", "CS B")],
    });
    const { wrapper } = await mountAt("C SCI ");
    expect(useCustomFetch).toHaveBeenCalledWith(
      "/api/v1/majors/details/C%20SCI",
    );
    const links = wrapper.findAll("a");
    expect(links).toHaveLength(2);
    expect(links[0].attributes("href")).toBe("/major?id=C+SCI-0-1-1");
  });

  it("redirects when a bare code has a single match", async () => {
    vi.mocked(useCustomFetch)
      .mockResolvedValueOnce({ matches: [match("MUSAP-0-1-8", "Music")] })
      .mockResolvedValueOnce({ credential_title: "Music" });
    const { wrapper, router } = await mountAt("MUSAP");
    await flushPromises();
    expect(router.currentRoute.value.query.id).toBe("MUSAP-0-1-8");
    expect(useCustomFetch).toHaveBeenLastCalledWith(
      "/api/v1/majors/details/MUSAP-0-1-8",
    );
    expect(wrapper.vm.major_data.credential_title).toBe("Music");
  });

  it("shows the error when no major is found", async () => {
    vi.mocked(useCustomFetch).mockRejectedValue(new Error("404"));
    const { wrapper } = await mountAt("NOPE");
    expect(wrapper.find(".alert").exists()).toBe(true);
  });
});
