import { flushPromises, mount } from "@vue/test-utils";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("@/composables/customFetch", () => ({ useCustomFetch: vi.fn() }));

import { useCustomFetch } from "@/composables/customFetch";
import Banner from "@/components/common/banner.vue";

describe("BannerComp", () => {
  beforeEach(() => {
    vi.mocked(useCustomFetch).mockReset();
    vi.mocked(useCustomFetch).mockResolvedValue({});
    delete window.show_coi;
  });

  afterEach(() => {
    vi.restoreAllMocks();
    delete window.show_coi;
  });

  it("is hidden by default", () => {
    const wrapper = mount(Banner);
    expect(wrapper.vm.show_coi).toBe(false);
    expect(wrapper.find(".alert").exists()).toBe(false);
  });

  it("renders the alert and sign-up link when show_coi is true", async () => {
    const wrapper = mount(Banner);
    await wrapper.setData({ show_coi: true });
    const alert = wrapper.find(".alert");
    expect(alert.exists()).toBe(true);
    expect(alert.text()).toContain("Join us as research participants!");
    const link = wrapper.find("a");
    expect(link.attributes("href")).toContain("docs.google.com/forms");
    expect(link.attributes("target")).toBe("_blank");
  });

  it("dismisses the banner and saves the user preference", async () => {
    const wrapper = mount(Banner);
    await wrapper.setData({ show_coi: true });

    await wrapper.find("button.btn-close").trigger("click");
    await flushPromises();

    expect(wrapper.vm.show_coi).toBe(false);
    expect(wrapper.find(".alert").exists()).toBe(false);
    expect(useCustomFetch).toHaveBeenCalledWith("/api/v1/user_pref/", {
      method: "POST",
      body: JSON.stringify({ viewed_coi_banner: true }),
      headers: { "Content-Type": "application/json" },
    });
  });

  it("still hides the banner when saving the preference fails", async () => {
    const errorSpy = vi.spyOn(console, "error").mockImplementation(() => {});
    vi.mocked(useCustomFetch).mockRejectedValue(new Error("boom"));

    const wrapper = mount(Banner);
    await wrapper.setData({ show_coi: true });

    await wrapper.vm.dismiss();
    await flushPromises();

    expect(wrapper.vm.show_coi).toBe(false);
    expect(errorSpy).toHaveBeenCalledWith(
      "Failed to save modal preference:",
      expect.any(Error),
    );
  });

  it("keeps the banner hidden on mount when window.show_coi is set", () => {
    window.show_coi = true;
    const wrapper = mount(Banner);
    expect(wrapper.vm.show_coi).toBe(false);
  });
});
