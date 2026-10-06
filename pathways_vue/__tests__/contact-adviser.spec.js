import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import ContactAdviser from "@/components/common/contact-adviser.vue";

const stubs = {
  BCard: { template: "<div class='b-card'><slot /></div>" },
};

const mountAdviser = (props) =>
  mount(ContactAdviser, { props, global: { stubs } });

describe("ContactAdviserCourse", () => {
  it("renders the heading with the given type", () => {
    const wrapper = mountAdviser({ campus: "Seattle", type: "major" });
    expect(wrapper.find("h2").text()).toBe("Are you considering this major?");
  });

  it("lists a single Tacoma adviser link (case-insensitive)", () => {
    const wrapper = mountAdviser({ campus: "TACOMA", type: "course" });
    const links = wrapper.findAll("a");
    expect(links).toHaveLength(1);
    expect(links[0].text()).toBe("Find your Tacoma adviser");
    expect(links[0].attributes("href")).toBe(
      "https://www.tacoma.uw.edu/gaa#permalink-37917",
    );
  });

  it("lists the three Seattle adviser links", () => {
    const wrapper = mountAdviser({ campus: "seattle", type: "major" });
    const links = wrapper.findAll("a");
    expect(links).toHaveLength(3);
    expect(links[0].text()).toBe("Find your premajor adviser");
    expect(links[2].attributes("href")).toBe(
      "https://advising.uw.edu/academic-support/advising-offices-by-program/",
    );
  });

  it("lists a single Bothell adviser link", () => {
    const wrapper = mountAdviser({ campus: "Bothell", type: "major" });
    const links = wrapper.findAll("a");
    expect(links).toHaveLength(1);
    expect(links[0].attributes("href")).toBe("https://uwb.navigate.eab.com/");
  });

  it("renders no links for an unknown campus", () => {
    const wrapper = mountAdviser({ campus: "Online", type: "major" });
    expect(wrapper.findAll("a")).toHaveLength(0);
    expect(wrapper.vm.advisingInfo).toEqual([]);
  });
});
