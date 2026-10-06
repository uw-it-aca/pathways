import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import CapacityDisplay from "@/components/major/capacity-display.vue";

const mountCapacity = (admissionType) =>
  mount(CapacityDisplay, { props: { admissionType } });

describe("MajorCapacityDisplay", () => {
  it.each([
    ["open", "Open", "bi-circle"],
    ["minimumRequirements", "Minimum Requirements", "bi-record-circle"],
    ["capacity-constrained", "Capacity Constrained", "bi-circle-fill"],
  ])(
    "renders text and icon for admission type '%s'",
    (admissionType, text, icon) => {
      const wrapper = mountCapacity(admissionType);
      expect(wrapper.text()).toBe(text);
      expect(wrapper.find("i").classes()).toContain(icon);
    },
  );

  it("falls back to 'Unknown Requirements' for an unrecognized type", () => {
    const wrapper = mountCapacity("something-else");
    expect(wrapper.text()).toBe("Unknown Requirements");
    expect(wrapper.find("i").classes()).toContain("bi-question-circle");
  });

  it("exposes the computed values via the component instance", () => {
    const wrapper = mountCapacity("open");
    expect(wrapper.vm.capacityText).toBe("Open");
    expect(wrapper.vm.capacityIcon).toBe("bi-circle");
  });
});
