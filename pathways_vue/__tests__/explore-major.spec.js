import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import ExploreMajor from "@/components/major/explore-major.vue";

const stubs = {
  SHeading: { template: "<div class='s-heading'><slot /></div>" },
};

const mountExplore = (major) =>
  mount(ExploreMajor, { props: { major }, global: { stubs } });

describe("ExploreMajor", () => {
  it("renders all three cards when every field is present", () => {
    const wrapper = mountExplore({
      program_code: "MATH",
      credential_code: "MATH-0-1-8",
      career_center_major: "mathematics",
    });
    const links = wrapper.findAll("a.card-link");
    expect(links).toHaveLength(3);
    expect(links[0].attributes("href")).toBe(
      "https://myplan.uw.edu/program/#/programs/MATH",
    );
    expect(links[1].attributes("href")).toBe(
      "https://myplan.uw.edu/program/#/programs/MATH/MATH-0-1-8",
    );
    expect(links[2].attributes("href")).toBe(
      "https://admit.washington.edu/majors/mathematics",
    );
  });

  it("renders only the program card when just program_code is set", () => {
    const wrapper = mountExplore({
      program_code: "MATH",
      credential_code: null,
      career_center_major: null,
    });
    const links = wrapper.findAll("a.card-link");
    expect(links).toHaveLength(1);
    expect(wrapper.text()).toContain("Program Information");
  });

  it("renders only the career card when just career_center_major is set", () => {
    const wrapper = mountExplore({
      program_code: null,
      credential_code: null,
      career_center_major: "mathematics",
    });
    const links = wrapper.findAll("a.card-link");
    expect(links).toHaveLength(1);
    expect(wrapper.text()).toContain("Career Outcomes");
    expect(links[0].attributes("href")).toBe(
      "https://admit.washington.edu/majors/mathematics",
    );
  });

  it("renders no cards when no fields are present", () => {
    const wrapper = mountExplore({
      program_code: null,
      credential_code: null,
      career_center_major: null,
    });
    expect(wrapper.findAll("a.card-link")).toHaveLength(0);
  });

  it("always renders the 'Explore this Major' heading", () => {
    const wrapper = mountExplore({
      program_code: null,
      credential_code: null,
      career_center_major: null,
    });
    expect(wrapper.find(".s-heading").text()).toBe("Explore this Major");
  });

  it("exposes empty URLs when the matching fields are null", () => {
    const wrapper = mountExplore({
      program_code: null,
      credential_code: null,
      career_center_major: null,
    });
    expect(wrapper.vm.myplanProgramURL).toBe("");
    expect(wrapper.vm.myplanCredentialURL).toBe("");
    expect(wrapper.vm.careerCenterOutcomeURL).toBe("");
  });
});
