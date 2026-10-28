import { mount } from "@vue/test-utils";
import { afterEach, beforeEach, describe, expect, it } from "vitest";

import RecentSearches from "@/components/search/recent-searches.vue";

describe("RecentSearches", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  afterEach(() => {
    localStorage.clear();
  });

  it("always renders the 'Recent Searches' heading", () => {
    const wrapper = mount(RecentSearches);
    expect(wrapper.find("h2").text()).toBe("Recent Searches");
  });

  it("shows the empty message when nothing is stored", () => {
    const wrapper = mount(RecentSearches);
    expect(wrapper.text()).toContain("No recent searches");
    expect(wrapper.find("ul").exists()).toBe(false);
  });

  it("renders a link for each stored search", () => {
    localStorage.setItem(
      "recentSearches",
      JSON.stringify(["music", "computer science"]),
    );
    const wrapper = mount(RecentSearches);
    const links = wrapper.findAll("a");
    expect(links).toHaveLength(2);
    expect(links[0].text()).toBe("music");
    expect(links[0].attributes("href")).toBe("/search?q=music");
  });

  it("URL-encodes search terms in the link href", () => {
    localStorage.setItem(
      "recentSearches",
      JSON.stringify(["computer science"]),
    );
    const wrapper = mount(RecentSearches);
    const link = wrapper.find("a");
    expect(link.attributes("href")).toBe("/search?q=computer%20science");
  });

  it("marks links as unmaskable for Clarity", () => {
    localStorage.setItem("recentSearches", JSON.stringify(["music"]));
    const wrapper = mount(RecentSearches);
    expect(wrapper.find("a").attributes("data-clarity-unmask")).toBe("true");
  });

  it("renders an empty list without the fallback message when storage is an empty array", () => {
    localStorage.setItem("recentSearches", JSON.stringify([]));
    const wrapper = mount(RecentSearches);
    // An empty array is truthy, so the list branch renders with no items
    expect(wrapper.find("ul").exists()).toBe(true);
    expect(wrapper.findAll("li")).toHaveLength(0);
    expect(wrapper.text()).not.toContain("No recent searches");
  });

  it("shows the empty message when stored value is null", () => {
    localStorage.setItem("recentSearches", JSON.stringify(null));
    const wrapper = mount(RecentSearches);
    expect(wrapper.text()).toContain("No recent searches");
  });
});
