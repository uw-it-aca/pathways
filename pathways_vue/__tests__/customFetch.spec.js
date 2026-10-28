import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

// Avoid the real token store (which reads a CSRF token from the DOM)
vi.mock("@/stores/token", () => ({
  useTokenStore: () => ({ csrfToken: "test-csrf-token" }),
}));

import { useCustomFetch } from "@/composables/customFetch";

const mockResponse = ({ ok = true, status = 200, text = "" }) => ({
  ok,
  status,
  text: () => Promise.resolve(text),
});

describe("useCustomFetch", () => {
  beforeEach(() => {
    global.fetch = vi.fn();
    vi.spyOn(console, "error").mockImplementation(() => {});
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("parses a successful JSON response", async () => {
    global.fetch.mockResolvedValue(
      mockResponse({ text: JSON.stringify({ credential_title: "Music" }) }),
    );
    const data = await useCustomFetch("/api/v1/majors/details/MUSAP");
    expect(data).toEqual({ credential_title: "Music" });
  });

  it("returns an empty object for an empty response body", async () => {
    global.fetch.mockResolvedValue(mockResponse({ text: "" }));
    const data = await useCustomFetch("/api/v1/empty");
    expect(data).toEqual({});
  });

  it("sends the default headers including the CSRF token", async () => {
    global.fetch.mockResolvedValue(mockResponse({ text: "{}" }));
    await useCustomFetch("/api/v1/thing");
    expect(global.fetch).toHaveBeenCalledWith(
      "/api/v1/thing",
      expect.objectContaining({
        headers: expect.objectContaining({
          "Access-Control-Allow-Origin": "*",
          "X-CSRFToken": "test-csrf-token",
          "X-Requested-With": "XMLHttpRequest",
        }),
      }),
    );
  });

  it("merges caller-provided headers and options with the defaults", async () => {
    global.fetch.mockResolvedValue(mockResponse({ text: "{}" }));
    await useCustomFetch("/api/v1/thing", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    const [, options] = global.fetch.mock.calls[0];
    expect(options.method).toBe("POST");
    expect(options.headers).toMatchObject({
      "X-CSRFToken": "test-csrf-token",
      "Content-Type": "application/json",
    });
  });

  it("throws when the response body is not valid JSON", async () => {
    global.fetch.mockResolvedValue(mockResponse({ text: "not json" }));
    await expect(useCustomFetch("/api/v1/bad")).rejects.toThrow(
      /Failed to parse response as JSON/,
    );
  });

  it("alerts and resolves to undefined on a 403", async () => {
    const alertSpy = vi
      .spyOn(window, "alert")
      .mockImplementation(() => {});
    global.fetch.mockResolvedValue(
      mockResponse({ ok: false, status: 403, text: "Forbidden" }),
    );
    const data = await useCustomFetch("/api/v1/secure");
    expect(data).toBeUndefined();
    expect(alertSpy).toHaveBeenCalledOnce();
  });

  it("throws an error carrying status and message for other non-ok responses", async () => {
    global.fetch.mockResolvedValue(
      mockResponse({ ok: false, status: 404, text: "Not Found" }),
    );
    await expect(useCustomFetch("/api/v1/missing")).rejects.toMatchObject({
      data: { status: 404, message: "Not Found" },
    });
  });

  it("rethrows and attaches data when the fetch itself rejects", async () => {
    global.fetch.mockRejectedValue(new Error("network down"));
    await expect(useCustomFetch("/api/v1/offline")).rejects.toMatchObject({
      message: "network down",
      data: { status: null, message: "network down" },
    });
    expect(console.error).toHaveBeenCalled();
  });
});
