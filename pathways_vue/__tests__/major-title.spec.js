import { flushPromises, mount } from "@vue/test-utils";
import { beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("@/composables/customFetch", () => ({ useCustomFetch: vi.fn() }));

import { useCustomFetch } from "@/composables/customFetch";
import MajorTitle from "@/components/common/major-title.vue";

const mountTitle = async (majorAbbrCode, props = {}) => {
  const wrapper = mount(MajorTitle, { props: { majorAbbrCode, ...props } });
  await flushPromises();
  return wrapper;
};

describe("MajorTitle", () => {
  beforeEach(() => {
    vi.mocked(useCustomFetch).mockReset();
  });

  it("renders majorName when no abbr code is given", async () => {
    const wrapper = await mountTitle("", { majorName: "Pre Sciences" });
    expect(wrapper.text()).toContain("Pre Sciences");
    expect(useCustomFetch).not.toHaveBeenCalled();
  });

  it("renders majorName when abbr code is only whitespace", async () => {
    const wrapper = await mountTitle("   ", { majorName: "Pre Sciences" });
    expect(wrapper.text()).toContain("Pre Sciences");
    expect(useCustomFetch).not.toHaveBeenCalled();
  });

  it("renders 'majorName (CODE)' when majorPremaj is true", async () => {
    const wrapper = await mountTitle("PSOCS", {
      majorPremaj: true,
      majorName: "Pre Sciences",
    });
    expect(wrapper.text()).toContain("Pre Sciences (PSOCS)");
    expect(useCustomFetch).not.toHaveBeenCalled();
  });

  it("trims the abbr code in the pre-major display", async () => {
    const wrapper = await mountTitle("  PSOCS  ", {
      majorPremaj: true,
      majorName: "Pre Sciences",
    });
    expect(wrapper.text()).toContain("Pre Sciences (PSOCS)");
    expect(useCustomFetch).not.toHaveBeenCalled();
  });

  it("renders a single credential title", async () => {
    vi.mocked(useCustomFetch).mockResolvedValue({
      credential_title: "Music",
    });
    const wrapper = await mountTitle("MUSAP-0-1-8");
    expect(useCustomFetch).toHaveBeenCalledWith(
      "/api/v1/majors/details/MUSAP-0-1-8",
    );
    expect(wrapper.text()).toContain("Music");
  });

  it("renders a title for each match of a bare code", async () => {
    vi.mocked(useCustomFetch)
      .mockResolvedValueOnce({
        matches: [
          { credential_code: "ACMS-0-1-1" },
          { credential_code: "ACMS-1-1-1" },
        ],
      })
      .mockResolvedValueOnce({ credential_title: "ACMS A" })
      .mockResolvedValueOnce({ credential_title: "ACMS B" });
    const wrapper = await mountTitle("ACMS");
    const divs = wrapper.findAll("div");
    const texts = divs.map((d) => d.text());
    expect(texts).toContain("ACMS A");
    expect(texts).toContain("ACMS B");
    expect(useCustomFetch).toHaveBeenCalledWith(
      "/api/v1/majors/details/ACMS-0-1-1",
    );
  });

  it("skips matches that fail to resolve", async () => {
    vi.mocked(useCustomFetch)
      .mockResolvedValueOnce({
        matches: [
          { credential_code: "ACMS-0-1-1" },
          { credential_code: "ACMS-1-1-1" },
        ],
      })
      .mockResolvedValueOnce({ credential_title: "ACMS A" })
      .mockRejectedValueOnce(new Error("404"));
    const wrapper = await mountTitle("ACMS");
    expect(wrapper.text()).toContain("ACMS A");
    expect(wrapper.vm.titles).toEqual(["ACMS A"]);
  });

  it("shows the error (abbr code) when no title is found", async () => {
    vi.mocked(useCustomFetch).mockResolvedValue({});
    const wrapper = await mountTitle("NOPE");
    expect(wrapper.vm.showError).toBe(true);
    expect(wrapper.text()).toContain("NOPE");
  });

  it("shows the error when the fetch rejects", async () => {
    vi.mocked(useCustomFetch).mockRejectedValue(new Error("boom"));
    const wrapper = await mountTitle("NOPE");
    expect(wrapper.vm.showError).toBe(true);
    expect(wrapper.text()).toContain("NOPE");
  });

  it("refetches when the abbr code prop changes", async () => {
    vi.mocked(useCustomFetch).mockResolvedValue({ credential_title: "Music" });
    const wrapper = await mountTitle("MUSAP-0-1-8");
    expect(wrapper.text()).toContain("Music");

    vi.mocked(useCustomFetch).mockResolvedValue({ credential_title: "Art" });
    await wrapper.setProps({ majorAbbrCode: "ARTAP-0-1-8" });
    await flushPromises();
    expect(useCustomFetch).toHaveBeenLastCalledWith(
      "/api/v1/majors/details/ARTAP-0-1-8",
    );
    expect(wrapper.text()).toContain("Art");
  });
});
