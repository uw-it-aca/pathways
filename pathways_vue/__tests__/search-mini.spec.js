import { mount } from "@vue/test-utils";
import { beforeEach, describe, expect, it, vi } from "vitest";

import SearchMini from "@/components/search/search-mini.vue";

const stubs = {
  BInputGroup: { template: "<div><slot /></div>" },
  BFormInput: {
    props: ["modelValue"],
    emits: ["update:modelValue", "focus", "keyup"],
    template:
      "<input :value='modelValue' @input=\"$emit('update:modelValue', $event.target.value)\" @focus=\"$emit('focus')\" @keyup.enter=\"$emit('keyup', $event)\" />",
  },
  BButton: { template: "<button><slot /></button>" },
  RecentSearches: { template: "<div class='recent-searches' />" },
  RecentViews: { template: "<div class='recent-views' />" },
};

const mountMini = (options = {}) => {
  const push = vi.fn();
  const wrapper = mount(SearchMini, {
    attachTo: options.attachTo,
    global: {
      stubs,
      mocks: { $router: { push } },
    },
  });
  return { wrapper, push };
};

describe("SearchMini", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("starts closed with the dropdown hidden", () => {
    const { wrapper } = mountMini();
    expect(wrapper.vm.open).toBe(false);
    const dropdown = wrapper.find("#search-mini-dropdown");
    expect(dropdown.isVisible()).toBe(false);
    expect(wrapper.find("input").attributes("aria-expanded")).toBe("false");
  });

  it("opens the dropdown when the input is focused", async () => {
    const { wrapper } = mountMini();
    await wrapper.find("input").trigger("focus");
    expect(wrapper.vm.open).toBe(true);
    expect(wrapper.find("#search-mini-dropdown").isVisible()).toBe(true);
    expect(wrapper.find("input").attributes("aria-expanded")).toBe("true");
  });

  it("navigates to the search page on button click", async () => {
    const { wrapper, push } = mountMini();
    await wrapper.find("input").setValue("music");
    await wrapper.find("button").trigger("click");
    expect(push).toHaveBeenCalledWith({
      path: "/search",
      query: { q: "music" },
    });
  });

  it("navigates on Enter and trims the query", async () => {
    const { wrapper, push } = mountMini();
    wrapper.vm.open = true;
    await wrapper.find("input").setValue("  music  ");
    await wrapper.find("input").trigger("keyup.enter");
    expect(push).toHaveBeenCalledWith({
      path: "/search",
      query: { q: "music" },
    });
    expect(wrapper.vm.open).toBe(false);
  });

  it("does not navigate when the query is blank", async () => {
    const { wrapper, push } = mountMini();
    await wrapper.find("input").setValue("   ");
    await wrapper.find("button").trigger("click");
    expect(push).not.toHaveBeenCalled();
  });

  it("closes when focus moves outside the component", () => {
    const { wrapper } = mountMini();
    wrapper.vm.open = true;
    wrapper.vm.onFocusOut({ relatedTarget: document.createElement("a") });
    expect(wrapper.vm.open).toBe(false);
  });

  it("stays open when focus moves to a child element", () => {
    const { wrapper } = mountMini();
    wrapper.vm.open = true;
    const child = wrapper.find("button").element;
    wrapper.vm.onFocusOut({ relatedTarget: child });
    expect(wrapper.vm.open).toBe(true);
  });

  it("closes via a real focusout DOM event when focus leaves the component", async () => {
    const outside = document.createElement("a");
    document.body.appendChild(outside);
    const { wrapper } = mountMini({ attachTo: document.body });
    wrapper.vm.open = true;
    await wrapper.vm.$nextTick();

    await wrapper.find(".dropdown").trigger("focusout", {
      relatedTarget: outside,
    });
    expect(wrapper.vm.open).toBe(false);

    wrapper.unmount();
    outside.remove();
  });

  it("stays open via a real focusout DOM event when focus stays inside", async () => {
    const { wrapper } = mountMini({ attachTo: document.body });
    wrapper.vm.open = true;
    await wrapper.vm.$nextTick();

    const child = wrapper.find("button").element;
    await wrapper.find(".dropdown").trigger("focusout", {
      relatedTarget: child,
    });
    expect(wrapper.vm.open).toBe(true);

    wrapper.unmount();
  });

  it("treats a focusout with no relatedTarget as leaving the component", () => {
    const { wrapper } = mountMini();
    wrapper.vm.open = true;
    wrapper.vm.onFocusOut({ relatedTarget: null });
    expect(wrapper.vm.open).toBe(false);
  });

  it("does not navigate on Enter when the query is blank", async () => {
    const { wrapper, push } = mountMini();
    wrapper.vm.open = true;
    await wrapper.find("input").setValue("   ");
    await wrapper.find("input").trigger("keyup.enter");
    expect(push).not.toHaveBeenCalled();
    // the dropdown stays open because navigation never happened
    expect(wrapper.vm.open).toBe(true);
  });

  it("renders the recent searches and recent views panels", () => {
    const { wrapper } = mountMini();
    expect(wrapper.find(".recent-searches").exists()).toBe(true);
    expect(wrapper.find(".recent-views").exists()).toBe(true);
  });

  it("prevents default on dropdown mousedown so the input keeps focus", async () => {
    const { wrapper } = mountMini();
    wrapper.vm.open = true;
    await wrapper.vm.$nextTick();
    const event = new MouseEvent("mousedown", {
      bubbles: true,
      cancelable: true,
    });
    wrapper.find("#search-mini-dropdown").element.dispatchEvent(event);
    expect(event.defaultPrevented).toBe(true);
  });
});
