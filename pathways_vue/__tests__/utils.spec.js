import { describe, expect, it } from "vitest";
import { preventWidow } from "@/utils";

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
