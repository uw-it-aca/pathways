import { describe, expect, it } from "vitest";
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
