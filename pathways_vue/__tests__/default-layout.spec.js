import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { afterEach, beforeEach, describe, expect, it } from "vitest";

import DefaultLayout from "@/layouts/default.vue";

const stubs = {
  // Render the named slots so slot content can be asserted
  STopbarNeo: {
    template:
      "<div class='topbar'><slot name='system' /><slot name='content' /><slot name='main' /><slot name='settings' /></div>",
  },
  SUser: { template: "<div><slot /><slot name='action' /></div>" },
  SColorMode: { template: "<div />" },
  BButton: { template: "<a><slot /></a>" },
};

const mountLayout = (pageTitle = "Majors", slotContent = "") =>
  mount(DefaultLayout, {
    props: { pageTitle },
    slots: slotContent ? { content: slotContent } : {},
    global: { stubs },
  });

describe("DefaultLayout (DawgPath)", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    // The context store reads initial state from this DOM element.
    // Use a non-executable element so jsdom doesn't try to run it as JS.
    const el = document.createElement("div");
    el.id = "django-context-data";
    el.textContent = JSON.stringify({
      user: "jdoe",
      login_user: "jdoe",
      override_user: null,
      signout_url: "/saml/logout",
    });
    document.body.appendChild(el);
    window.pathways = undefined;
  });

  afterEach(() => {
    document.getElementById("django-context-data")?.remove();
    window.pathways = undefined;
  });

  it("mounts and has the correct component name", () => {
    const wrapper = mountLayout();
    expect(wrapper.vm.$options.name).toBe("DawgPath");
    expect(wrapper.find(".topbar").exists()).toBe(true);
  });

  it("sets the document title to 'Page Title - AppName'", () => {
    mountLayout("Majors");
    expect(document.title).toBe("Majors - DawgPath");
  });

  it("renders content passed into the content slot", () => {
    const wrapper = mountLayout("Home", "<p class='child'>Hello</p>");
    expect(wrapper.find(".child").text()).toBe("Hello");
  });

  it("returns an empty array when there are no system messages", () => {
    const wrapper = mountLayout();
    expect(wrapper.vm.systemMessages).toEqual([]);
  });

  it("exposes system messages from window.pathways.messages", () => {
    window.pathways = { messages: ["Scheduled maintenance tonight"] };
    const wrapper = mountLayout();
    expect(wrapper.vm.systemMessages).toEqual([
      "Scheduled maintenance tonight",
    ]);
    expect(wrapper.text()).toContain("Scheduled maintenance tonight");
  });

  it("shows the preferred first name when available on personData", () => {
    document.getElementById("django-context-data").textContent =
      JSON.stringify({
        user: "jdoe",
        login_user: "jdoe",
        personData: { preferred_first_name: "Jamie", uwnetid: "jdoe" },
      });
    const wrapper = mountLayout();
    expect(wrapper.text()).toContain("Jamie");
    expect(wrapper.text()).not.toContain("jdoe");
  });

  it("falls back to uwnetid when preferred first name is not available", () => {
    document.getElementById("django-context-data").textContent =
      JSON.stringify({
        user: "jdoe",
        login_user: "jdoe",
        personData: { uwnetid: "jdoe" },
      });
    const wrapper = mountLayout();
    expect(wrapper.text()).toContain("jdoe");
  });

  describe("user override", () => {
    const setContext = (extra = {}) => {
      document.getElementById("django-context-data").textContent =
        JSON.stringify({
          user: "jdoe",
          login_user: "jdoe",
          signout_url: "/saml/logout",
          personData: { uwnetid: "jdoe" },
          ...extra,
        });
    };

    it.each([
      ["null", null],
      ["empty string", ""],
      ["undefined", undefined],
      ["same as login user", "jdoe"],
    ])("isOverriding is false when override_user is %s", (_, value) => {
      setContext({ override_user: value });
      const wrapper = mountLayout();
      expect(wrapper.vm.isOverriding).toBe(false);
    });

    it("isOverriding is true when override_user differs from login_user", () => {
      setContext({ override_user: "billy" });
      const wrapper = mountLayout();
      expect(wrapper.vm.isOverriding).toBe(true);
    });

    it("shows the sign out link and no clear override link without an override", () => {
      setContext({ override_user: null });
      const wrapper = mountLayout();
      expect(wrapper.find("a[href='/support/']").exists()).toBe(false);
      expect(wrapper.find("a[href='/saml/logout']").exists()).toBe(true);
      expect(wrapper.text()).not.toContain("Clear override");
    });

    it("shows the clear override link instead of sign out when overriding", () => {
      setContext({ override_user: "billy" });
      const wrapper = mountLayout();
      const clear = wrapper.find("a[href='/support/']");
      expect(clear.exists()).toBe(true);
      expect(clear.text()).toContain("Clear override");
    });
  });
});
