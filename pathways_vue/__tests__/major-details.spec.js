import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import MajorDetails from "@/components/major/major-details.vue";

const stubs = {
  SHeading: {
    template: "<h1 data-clarity-unmask='true'><slot /></h1>",
  },
  MajorCapacityDisplay: {
    name: "MajorCapacityDisplay",
    props: ["admissionType"],
    template: "<span class='capacity'>{{ admissionType }}</span>",
  },
};

const major = {
  credential_title: "Computer Science",
  major_school: "Engineering",
  major_campus: "Seattle",
  major_admission: "capacity-constrained",
  credential_description: "<em>Study computing</em>",
};

const mountDetails = (overrides = {}) =>
  mount(MajorDetails, {
    props: { major: { ...major, ...overrides } },
    global: { stubs },
  });

describe("MajorDetails", () => {
  it("renders the credential title in the heading", () => {
    const wrapper = mountDetails();
    const heading = wrapper.find("h1");
    expect(heading.text()).toBe("Computer Science");
    expect(heading.attributes("data-clarity-unmask")).toBe("true");
  });

  it("renders the school and campus", () => {
    const wrapper = mountDetails();
    expect(wrapper.text()).toContain("Engineering - Seattle");
  });

  it("links the admission type to the FAQ and passes it to the capacity display", () => {
    const wrapper = mountDetails();
    const link = wrapper.find("a[href='/faq#admission_types']");
    expect(link.exists()).toBe(true);
    const capacity = wrapper.findComponent({ name: "MajorCapacityDisplay" });
    expect(capacity.props("admissionType")).toBe("capacity-constrained");
  });

  it("renders the credential description as raw HTML", () => {
    const wrapper = mountDetails();
    const description = wrapper.find(".major-description");
    expect(description.html()).toContain("<em>Study computing</em>");
  });
});
