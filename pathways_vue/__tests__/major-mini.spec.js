import { flushPromises, mount } from "@vue/test-utils";
import { beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("@/composables/customFetch", () => ({ useCustomFetch: vi.fn() }));

import { useCustomFetch } from "@/composables/customFetch";
import MajorMini from "@/components/common/major-mini.vue";

const stubs = {
  BCard: { template: "<div class='b-card'><slot /></div>" },
  BLink: {
    name: "BLink",
    props: ["to"],
    template: "<a class='b-link'><slot /></a>",
  },
  SHeading: { template: "<h3><slot /></h3>" },
  MajorCapacityDisplay: { template: "<span class='capacity' />" },
};

const major = (code, title) => ({
  credential_code: code,
  credential_title: title,
  major_school: "Arts",
  major_campus: "Seattle",
  major_admission: "open",
});

const mountMini = async (majorAbbrCode) => {
  const wrapper = mount(MajorMini, {
    props: { majorAbbrCode },
    global: { stubs },
  });
  await flushPromises();
  return wrapper;
};

describe("MajorMini", () => {
  beforeEach(() => {
    vi.mocked(useCustomFetch).mockReset();
  });

  it("shows an error when no abbr code is given", async () => {
    const wrapper = await mountMini("");
    expect(wrapper.vm.showError).toBe(true);
    expect(wrapper.text()).toContain("Data is not available for major");
    expect(useCustomFetch).not.toHaveBeenCalled();
  });

  it("renders a card for a single credential code", async () => {
    vi.mocked(useCustomFetch).mockResolvedValue(major("MUSAP-0-1-8", "Music"));
    const wrapper = await mountMini("MUSAP-0-1-8");
    expect(useCustomFetch).toHaveBeenCalledWith(
      "/api/v1/majors/details/MUSAP-0-1-8",
    );
    expect(wrapper.text()).toContain("Music");
    expect(wrapper.text()).toContain("Arts - Seattle");
    expect(wrapper.findAll(".b-card")).toHaveLength(1);
  });

  it("renders a card for each match of a bare code", async () => {
    vi.mocked(useCustomFetch)
      .mockResolvedValueOnce({
        matches: [
          { credential_code: "ACMS-0-1-1" },
          { credential_code: "ACMS-1-1-1" },
        ],
      })
      .mockResolvedValueOnce(major("ACMS-0-1-1", "ACMS A"))
      .mockResolvedValueOnce(major("ACMS-1-1-1", "ACMS B"));
    const wrapper = await mountMini("ACMS");
    expect(wrapper.findAll(".b-card")).toHaveLength(2);
    expect(wrapper.text()).toContain("ACMS\u00A0A");
    expect(wrapper.text()).toContain("ACMS\u00A0B");
  });

  it("skips matches that fail to resolve", async () => {
    vi.mocked(useCustomFetch)
      .mockResolvedValueOnce({
        matches: [
          { credential_code: "ACMS-0-1-1" },
          { credential_code: "ACMS-1-1-1" },
        ],
      })
      .mockResolvedValueOnce(major("ACMS-0-1-1", "ACMS A"))
      .mockRejectedValueOnce(new Error("404"));
    const wrapper = await mountMini("ACMS");
    expect(wrapper.findAll(".b-card")).toHaveLength(1);
    expect(wrapper.vm.majors).toHaveLength(1);
    expect(wrapper.text()).toContain("ACMS\u00A0A");
  });

  it("trims whitespace and encodes the abbr code", async () => {
    vi.mocked(useCustomFetch).mockResolvedValue({
      matches: [{ credential_code: "C SCI-0-1-1" }],
    });
    await mountMini("C SCI ");
    expect(useCustomFetch).toHaveBeenCalledWith(
      "/api/v1/majors/details/C%20SCI",
    );
  });

  it("builds a 'Learn more' link to the major detail route", async () => {
    vi.mocked(useCustomFetch).mockResolvedValue(major("MUSAP-0-1-8", "Music"));
    const wrapper = await mountMini("MUSAP-0-1-8");
    const link = wrapper.findComponent({ name: "BLink" });
    expect(link.props("to")).toEqual({
      path: "/major",
      query: { id: "MUSAP-0-1-8" },
    });
  });

  it("shows the error when the fetch rejects", async () => {
    vi.mocked(useCustomFetch).mockRejectedValue(new Error("boom"));
    const wrapper = await mountMini("NOPE");
    expect(wrapper.vm.showError).toBe(true);
    expect(wrapper.text()).toContain("Data is not available for major");
    expect(wrapper.text()).toContain("NOPE");
  });

  it("refetches when the abbr code prop changes", async () => {
    vi.mocked(useCustomFetch).mockResolvedValue(major("MUSAP-0-1-8", "Music"));
    const wrapper = await mountMini("MUSAP-0-1-8");
    expect(wrapper.text()).toContain("Music");

    vi.mocked(useCustomFetch).mockResolvedValue(major("ARTAP-0-1-8", "Art"));
    await wrapper.setProps({ majorAbbrCode: "ARTAP-0-1-8" });
    await flushPromises();
    expect(useCustomFetch).toHaveBeenLastCalledWith(
      "/api/v1/majors/details/ARTAP-0-1-8",
    );
    expect(wrapper.text()).toContain("Art");
  });
});
