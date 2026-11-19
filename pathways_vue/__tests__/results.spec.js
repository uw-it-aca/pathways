import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import Results from "@/components/search/results.vue";

const courses = (count) =>
  Array.from({ length: count }, (_, i) => ({
    id: `CSE ${100 + i}`,
    is_course: true,
    title: `Course ${i}`,
    url: `/course?id=CSE ${100 + i}`,
    campus: "seattle",
    description: `Description ${i}`,
  }));

const mountResults = (search_results) =>
  mount(Results, { props: { search_results } });

const renderedIds = (wrapper) =>
  wrapper.findAll("li.mb-3 a span").map((span) => span.text());

describe("Search results", () => {
  it("renders majors and courses with links, campus, and description", () => {
    const wrapper = mountResults([
      {
        id: "MUSIC-10-1-1",
        is_major: true,
        title: "Music",
        url: "/major?id=MUSIC-10-1-1",
        campus: "seattle",
        description: "Study music.",
      },
      ...courses(1),
    ]);

    expect(wrapper.find("h2").text()).toBe("2 results");
    const items = wrapper.findAll("li.mb-3");
    expect(items[0].find("a").text()).toBe("Music");
    expect(items[0].find("a").attributes("href")).toBe(
      "/major?id=MUSIC-10-1-1",
    );
    expect(items[0].text()).toContain("seattle");
    expect(items[0].text()).toContain("Study music.");
    expect(items[1].find("a").text()).toBe("CSE 100 Course 0");
    expect(items[1].text()).toContain("Description 0");
  });

  it("paginates thirty results per page", async () => {
    const wrapper = mountResults(courses(65));

    expect(wrapper.find("h2").text()).toBe("65 results");
    expect(renderedIds(wrapper)).toHaveLength(30);
    const pageLinks = wrapper.findAll("a.page-link:not([aria-label])");
    expect(pageLinks.map((link) => link.text())).toEqual(["1", "2", "3"]);
    expect(pageLinks[0].classes()).toContain("active");

    await pageLinks[2].trigger("click");
    expect(renderedIds(wrapper)).toEqual([
      "CSE 160",
      "CSE 161",
      "CSE 162",
      "CSE 163",
      "CSE 164",
    ]);
    expect(
      wrapper.findAll("a.page-link:not([aria-label])")[2].classes(),
    ).toContain("active");
  });

  it("keeps previous and next within the available pages", async () => {
    const wrapper = mountResults(courses(31));
    const previous = wrapper.find("a[aria-label='Previous']");
    const next = wrapper.find("a[aria-label='Next']");

    await previous.trigger("click");
    expect(wrapper.vm.page).toBe(1);
    await next.trigger("click");
    expect(wrapper.vm.page).toBe(2);
    expect(renderedIds(wrapper)).toEqual(["CSE 130"]);
    await next.trigger("click");
    expect(wrapper.vm.page).toBe(2);
    await previous.trigger("click");
    expect(wrapper.vm.page).toBe(1);
  });

  it("returns to the first page when the results change", async () => {
    const wrapper = mountResults(courses(65));
    await wrapper.find("a[aria-label='Next']").trigger("click");
    expect(wrapper.vm.page).toBe(2);

    await wrapper.setProps({ search_results: courses(40) });
    expect(wrapper.vm.page).toBe(1);
    expect(renderedIds(wrapper)[0]).toBe("CSE 100");
  });

  it("shows zero results and no page links for an empty list", () => {
    const wrapper = mountResults([]);
    expect(wrapper.find("h2").text()).toBe("0 results");
    expect(wrapper.findAll("li.mb-3")).toHaveLength(0);
    expect(wrapper.findAll("a.page-link:not([aria-label])")).toHaveLength(0);
  });
});
