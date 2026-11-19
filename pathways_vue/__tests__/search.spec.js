import { flushPromises, mount } from "@vue/test-utils";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { createMemoryHistory, createRouter } from "vue-router";

vi.mock("@/composables/customFetch", () => ({ useCustomFetch: vi.fn() }));

import { useCustomFetch } from "@/composables/customFetch";
import Search from "@/pages/search.vue";

const resultsFor = (overrides = {}) =>
  Search.computed.search_results.call({
    major_matches: [],
    course_matches: [],
    text_matches: [],
    form_data: { type: "all", campus: "all" },
    ...overrides,
  });

describe("Search result merging", () => {
  it("keeps the exact course match ahead of overlapping text matches", () => {
    const exact = {
      id: "CSE 142",
      is_course: true,
      campus: "seattle",
      score: 100,
    };
    const related = { id: "CSE 143", is_course: true, campus: "seattle" };
    expect(
      resultsFor({
        course_matches: [exact],
        text_matches: [{ ...exact, score: 16 }, related],
      }),
    ).toEqual([exact, related]);
  });

  it("keeps different entity types and campuses distinct", () => {
    const course = { id: "TEST", is_course: true, campus: "seattle" };
    const major = { id: "TEST", is_major: true, campus: "seattle" };
    const otherCampus = { ...course, campus: "bothell" };
    expect(
      resultsFor({
        major_matches: [major],
        course_matches: [course],
        text_matches: [{ ...major }, otherCampus],
      }),
    ).toEqual([major, course, otherCampus]);
  });
});

describe("Search result filters", () => {
  const course = { id: "CSE 142", is_course: true, campus: "Seattle" };
  const major = { id: "CSE-10-1-1", is_major: true, campus: "Bothell" };

  it("filters by type and campus", () => {
    const matches = { course_matches: [course], major_matches: [major] };
    expect(
      resultsFor({ ...matches, form_data: { type: "course", campus: "all" } }),
    ).toEqual([course]);
    expect(
      resultsFor({ ...matches, form_data: { type: "major", campus: "all" } }),
    ).toEqual([major]);
    expect(
      resultsFor({ ...matches, form_data: { type: "all", campus: "bothell" } }),
    ).toEqual([major]);
  });

  it("treats results without a campus as campus-less", () => {
    const noCampus = { id: "ART 101", is_course: true };
    expect(
      resultsFor({
        course_matches: [noCampus],
        text_matches: [{ ...noCampus }],
      }),
    ).toEqual([noCampus]);
    expect(
      resultsFor({
        course_matches: [noCampus],
        form_data: { type: "all", campus: "seattle" },
      }),
    ).toEqual([]);
  });
});

const response = {
  major_matches: [{ id: "MUSIC-10-1-1", is_major: true, campus: "seattle" }],
  course_matches: [{ id: "MUSIC 120", is_course: true, campus: "seattle" }],
  text_matches: [],
};

const mountSearch = async (query = {}) => {
  const router = createRouter({
    history: createMemoryHistory(),
    routes: [{ path: "/search", component: Search }],
  });
  router.push({ path: "/search", query });
  await router.isReady();
  const wrapper = mount(Search, {
    attachTo: document.body,
    global: {
      plugins: [router],
      stubs: {
        DefaultLayout: { template: "<div><slot name='content' /></div>" },
        SHeading: { template: "<h1><slot /></h1>" },
        RecentSearches: { template: "<div class='recent-searches' />" },
        RecentViews: { template: "<div class='recent-views' />" },
        SearchResults: {
          props: ["search_results"],
          template: "<div class='search-results' />",
        },
      },
    },
  });
  await flushPromises();
  return { wrapper, router };
};

const lastSearchParams = () =>
  new URLSearchParams(vi.mocked(useCustomFetch).mock.lastCall[0].split("?")[1]);

describe("Search page", () => {
  let wrapper;

  beforeEach(() => {
    localStorage.clear();
    vi.mocked(useCustomFetch).mockReset();
    vi.mocked(useCustomFetch).mockResolvedValue(response);
  });

  afterEach(() => {
    wrapper?.unmount();
  });

  it("shows recent searches and views before searching", async () => {
    ({ wrapper } = await mountSearch());
    expect(useCustomFetch).not.toHaveBeenCalled();
    expect(wrapper.find(".recent-searches").exists()).toBe(true);
    expect(wrapper.find(".recent-views").exists()).toBe(true);
    expect(wrapper.find(".search-results").exists()).toBe(false);
  });

  it("runs the search from the q query parameter on load", async () => {
    ({ wrapper } = await mountSearch({ q: "music" }));
    expect(useCustomFetch).toHaveBeenCalledTimes(1);
    expect(lastSearchParams().get("search_string")).toBe("music");
    expect(lastSearchParams().has("type[]")).toBe(false);
    expect(lastSearchParams().has("campus[]")).toBe(false);
    const results = wrapper.findComponent(".search-results");
    expect(results.props("search_results")).toEqual([
      ...response.major_matches,
      ...response.course_matches,
    ]);
    expect(JSON.parse(localStorage.getItem("recentSearches"))).toEqual([
      "music",
    ]);
  });

  it("submits the typed search and syncs the q query parameter", async () => {
    let router;
    ({ wrapper, router } = await mountSearch());
    await wrapper.find("#search-string").setValue("  art  ");
    await flushPromises();
    expect(router.currentRoute.value.query.q).toBe("art");

    await wrapper.find("#button-addon2").trigger("click");
    await flushPromises();
    expect(lastSearchParams().get("search_string")).toBe("  art  ");
    expect(wrapper.find(".search-results").exists()).toBe(true);

    await wrapper.find("#search-string").setValue("");
    await flushPromises();
    expect(router.currentRoute.value.query.q).toBeUndefined();
  });

  it("re-runs the search with type and campus filters", async () => {
    ({ wrapper } = await mountSearch({ q: "music" }));
    await wrapper.find("#courseType").setValue();
    await flushPromises();
    expect(lastSearchParams().getAll("type[]")).toEqual(["course"]);

    await wrapper.find("#tacomaCampus").setValue();
    await flushPromises();
    expect(lastSearchParams().getAll("type[]")).toEqual(["course"]);
    expect(lastSearchParams().getAll("campus[]")).toEqual(["tacoma"]);
    expect(useCustomFetch).toHaveBeenCalledTimes(3);
  });

  it("applies every type and campus option", async () => {
    ({ wrapper } = await mountSearch({ q: "music" }));
    const options = [
      ["#majorType", "type[]", ["major"]],
      ["#allType", "type[]", []],
      ["#seattleCampus", "campus[]", ["seattle"]],
      ["#bothellCampus", "campus[]", ["bothell"]],
      ["#allCampus", "campus[]", []],
    ];
    for (const [selector, param, expected] of options) {
      await wrapper.find(selector).setValue();
      await flushPromises();
      expect(lastSearchParams().getAll(param)).toEqual(expected);
    }
  });

  it("records a failed search without showing results", async () => {
    vi.mocked(useCustomFetch).mockRejectedValue(new Error("offline"));
    ({ wrapper } = await mountSearch({ q: "music" }));
    expect(wrapper.vm.search_error).toBe(true);
    expect(wrapper.vm.has_searched).toBe(false);
    expect(wrapper.find(".recent-searches").exists()).toBe(true);
  });

  it("clears results and returns focus to the search input", async () => {
    ({ wrapper } = await mountSearch({ q: "music" }));
    await wrapper.find("button.btn-link").trigger("click");
    await flushPromises();

    expect(wrapper.vm.form_data.search_string).toBe("");
    expect(wrapper.vm.search_results).toEqual([]);
    expect(wrapper.find(".recent-searches").exists()).toBe(true);
    expect(document.activeElement).toBe(wrapper.find("#search-string").element);
  });

  it("keeps the five most recent unique searches", async () => {
    localStorage.setItem(
      "recentSearches",
      JSON.stringify(["a", "b", "c", "d", "e"]),
    );
    ({ wrapper } = await mountSearch());
    wrapper.vm.addToRecent("");
    wrapper.vm.addToRecent("c");
    expect(JSON.parse(localStorage.getItem("recentSearches"))).toEqual([
      "a",
      "b",
      "c",
      "d",
      "e",
    ]);
    wrapper.vm.addToRecent("f");
    expect(JSON.parse(localStorage.getItem("recentSearches"))).toEqual([
      "f",
      "a",
      "b",
      "c",
      "d",
    ]);
  });
});
