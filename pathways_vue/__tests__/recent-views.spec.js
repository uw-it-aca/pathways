import { mount } from "@vue/test-utils";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import RecentViews from "@/components/search/recent-views.vue";

describe("RecentViews", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    localStorage.clear();
  });

  it("always renders the 'Recently Viewed' heading", () => {
    const wrapper = mount(RecentViews);
    expect(wrapper.find("h2").text()).toBe("Recently Viewed");
  });

  it("shows the empty message when nothing is stored", () => {
    const wrapper = mount(RecentViews);
    expect(wrapper.text()).toContain("No courses or majors recently viewed");
    expect(wrapper.find("ul").exists()).toBe(false);
  });

  it("renders a link for each stored view", () => {
    const views = [
      { url: "/major?id=MUSAP", title: "Music", campus: "Seattle" },
      { url: "/course?id=CSE142", title: "CSE 142", campus: "Tacoma" },
    ];
    localStorage.setItem("recentViews", JSON.stringify(views));

    const wrapper = mount(RecentViews);
    const links = wrapper.findAll("a.recent_view_link");
    expect(links).toHaveLength(2);

    expect(links[0].attributes("href")).toBe("/major?id=MUSAP");
    expect(links[0].text()).toContain("Music");
    expect(links[0].text()).toContain("Seattle");

    expect(links[1].attributes("href")).toBe("/course?id=CSE142");
    expect(links[1].text()).toContain("CSE 142");
    expect(links[1].text()).toContain("Tacoma");

    expect(wrapper.find(".badge").exists()).toBe(true);
  });

  it("renders an empty list without the fallback message when storage is an empty array", () => {
    localStorage.setItem("recentViews", JSON.stringify([]));
    const wrapper = mount(RecentViews);
    // An empty array is truthy, so the list branch renders with no items
    expect(wrapper.find("ul").exists()).toBe(true);
    expect(wrapper.findAll("li")).toHaveLength(0);
    expect(wrapper.text()).not.toContain(
      "No courses or majors recently viewed",
    );
  });

  it("shows the empty message when stored value is null", () => {
    localStorage.setItem("recentViews", JSON.stringify(null));
    const wrapper = mount(RecentViews);
    expect(wrapper.text()).toContain("No courses or majors recently viewed");
  });

  it("marks links as unmaskable for Clarity", () => {
    localStorage.setItem(
      "recentViews",
      JSON.stringify([{ url: "/x", title: "X", campus: "Bothell" }]),
    );
    const wrapper = mount(RecentViews);
    expect(wrapper.find("a.recent_view_link").attributes("data-clarity-unmask")).toBe(
      "true",
    );
  });
});
