import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { preventWidow } from "@/utils";
import utils from "@/utils";

describe("preventWidow", () => {
  it("replaces the last space with a non-breaking space", () => {
    expect(preventWidow("ACMS A")).toBe("ACMS\u00A0A");
  });

  it("only replaces the space before the final word in multi-word strings", () => {
    expect(preventWidow("Bachelor of Arts in Music")).toBe(
      "Bachelor of Arts in\u00A0Music",
    );
  });

  it("returns single-word strings unchanged", () => {
    expect(preventWidow("Music")).toBe("Music");
  });

  it("returns an empty string unchanged", () => {
    expect(preventWidow("")).toBe("");
  });

  it("returns non-string input unchanged", () => {
    expect(preventWidow(null)).toBe(null);
    expect(preventWidow(undefined)).toBe(undefined);
  });

  it("collapses multiple trailing spaces into a single non-breaking space", () => {
    expect(preventWidow("Music   Degree")).toBe("Music\u00A0Degree");
  });
});

describe("recentViewManager", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  afterEach(() => {
    localStorage.clear();
  });

  it("adds a new view to an empty list", () => {
    utils.recentViewManager("Informatics", "/majors/informatics", "Seattle");
    const stored = JSON.parse(localStorage.getItem("recentViews"));
    expect(stored).toEqual([
      { title: "Informatics", url: "/majors/informatics", campus: "Seattle" },
    ]);
  });

  it("adds new views to the front of the list", () => {
    utils.recentViewManager("Informatics", "/majors/informatics", "Seattle");
    utils.recentViewManager("Biology", "/majors/biology", "Seattle");
    const stored = JSON.parse(localStorage.getItem("recentViews"));
    expect(stored[0]).toEqual({
      title: "Biology",
      url: "/majors/biology",
      campus: "Seattle",
    });
    expect(stored[1]).toEqual({
      title: "Informatics",
      url: "/majors/informatics",
      campus: "Seattle",
    });
  });

  it("does not add a duplicate entry for an existing url", () => {
    utils.recentViewManager("Informatics", "/majors/informatics", "Seattle");
    utils.recentViewManager("Informatics", "/majors/informatics", "Seattle");
    const stored = JSON.parse(localStorage.getItem("recentViews"));
    expect(stored).toHaveLength(1);
  });

  it("keeps only the 5 most recent views", () => {
    for (let i = 0; i < 6; i++) {
      utils.recentViewManager(`Major ${i}`, `/majors/${i}`, "Seattle");
    }
    const stored = JSON.parse(localStorage.getItem("recentViews"));
    expect(stored).toHaveLength(5);
    expect(stored[0]).toEqual({
      title: "Major 5",
      url: "/majors/5",
      campus: "Seattle",
    });
  });
});
