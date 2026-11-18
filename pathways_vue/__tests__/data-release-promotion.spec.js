import { flushPromises, mount } from "@vue/test-utils";
import { afterEach, describe, expect, it, vi } from "vitest";

import DataReleasePromotion from "@/support/data-release-promotion.vue";

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe("DataReleasePromotion", () => {
  it("disables promotion only for the current selected release", async () => {
    const releases = [
      { release_id: "current", manifest_size: 100 },
      { release_id: "other", manifest_size: 100 },
    ];
    vi.stubGlobal("fetch", vi.fn().mockImplementation((url) => Promise.resolve({
      ok: true,
      json: async () => url.endsWith("/manifest/")
        ? { success: true, manifest: { artifacts: {} } }
        : { success: true, releases, current_release_id: "current" },
    })));
    const wrapper = mount(DataReleasePromotion);
    await flushPromises();
    await wrapper.findAll(".list-group-item")[0].trigger("click");
    await flushPromises();
    expect(wrapper.find(".btn-primary").element.disabled).toBe(true);
    await wrapper.findAll(".list-group-item")[1].trigger("click");
    await flushPromises();
    expect(wrapper.find(".btn-primary").element.disabled).toBe(false);
    wrapper.unmount();
  });

  it.each([
    ["release-001", true],
    ["release-not-listed", false],
    [null, false],
  ])("shows current release %s even when not in the list", async (currentReleaseId, hasBadge) => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        success: true,
        releases: [{ release_id: "release-001", manifest_size: 100 }],
        current_release_id: currentReleaseId,
      }),
    }));

    const wrapper = mount(DataReleasePromotion);
    await flushPromises();
    expect(wrapper.text()).toContain("Current imported release:");
    expect(wrapper.text()).toContain(currentReleaseId || "Unknown");
    expect(wrapper.find(".badge").exists()).toBe(hasBadge);
    wrapper.unmount();
  });

  it("refreshes the current release from the server", async () => {
    const response = (currentReleaseId) => ({
      ok: true,
      json: async () => ({ success: true, releases: [], current_release_id: currentReleaseId }),
    });
    vi.stubGlobal("fetch", vi.fn()
      .mockResolvedValueOnce(response("previous"))
      .mockResolvedValueOnce(response("imported")));
    const wrapper = mount(DataReleasePromotion);
    await flushPromises();
    expect(wrapper.text()).toContain("previous");
    await wrapper.findAll("button").find((button) => button.text() === "Refresh").trigger("click");
    await flushPromises();
    expect(wrapper.text()).toContain("imported");
    expect(wrapper.text()).not.toContain("previous");
    wrapper.unmount();
  });

  it("shows and dismisses a release-list API error", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ success: false }),
    }));

    const wrapper = mount(DataReleasePromotion);
    await flushPromises();

    expect(wrapper.find('[role="alert"]').text()).toContain("Failed to load releases");
    await wrapper.find('[aria-label="Dismiss error"]').trigger("click");
    expect(wrapper.find('[role="alert"]').exists()).toBe(false);
    expect(wrapper.text()).toContain("No data releases available.");
    wrapper.unmount();
  });

  it("shows a release-list network error", async () => {
    vi.spyOn(console, "error").mockImplementation(() => {});
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));

    const wrapper = mount(DataReleasePromotion);
    await flushPromises();

    expect(wrapper.find('[role="alert"]').text()).toContain(
      "Failed to load releases: offline",
    );
    wrapper.unmount();
  });

  it("shows an HTTP error when the release list cannot be loaded", async () => {
    vi.spyOn(console, "error").mockImplementation(() => {});
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: false,
      status: 503,
    }));

    const wrapper = mount(DataReleasePromotion);
    await flushPromises();

    expect(wrapper.find('[role="alert"]').text()).toContain(
      "Failed to load releases: HTTP 503",
    );
    wrapper.unmount();
  });

  it("shows manifest API errors and supports refreshing details", async () => {
    vi.spyOn(console, "error").mockImplementation(() => {});
    const release = { release_id: "release-001", manifest_size: 100 };
    const fetch = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, releases: [release] }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: false }),
      })
      .mockResolvedValueOnce({ ok: false, status: 404 });
    vi.stubGlobal("fetch", fetch);

    const wrapper = mount(DataReleasePromotion);
    await flushPromises();
    await wrapper.find(".list-group-item").trigger("click");
    await flushPromises();
    expect(wrapper.find('[role="alert"]').text()).toContain("Failed to load manifest");

    await wrapper.find('[aria-label="Dismiss error"]').trigger("click");
    await wrapper.findAll("button").find((button) =>
      button.text() === "Refresh Details",
    ).trigger("click");
    await flushPromises();
    expect(wrapper.find('[role="alert"]').text()).toContain(
      "Failed to load manifest: HTTP 404",
    );
    expect(fetch).toHaveBeenCalledTimes(3);
    wrapper.unmount();
  });

  it("renders manifest artifact metadata and formats dates and sizes", async () => {
    const release = {
      release_id: "release-001",
      manifest_size: 2048,
      updated: "2026-11-06T10:00:00Z",
    };
    vi.stubGlobal("fetch", vi.fn().mockImplementation((url) => Promise.resolve({
      ok: true,
      json: async () => url.endsWith("/manifest/")
        ? {
          success: true,
          manifest: {
            schema_version: "2.0",
            artifacts: {
              "course_data.json": {
                size_bytes: 1024,
                checksum_sha256: "123456789abcdef",
              },
            },
          },
        }
        : { success: true, releases: [release] },
    })));

    const wrapper = mount(DataReleasePromotion);
    await flushPromises();
    await wrapper.find(".list-group-item").trigger("click");
    await flushPromises();

    expect(wrapper.text()).toContain("Schema: 2.0");
    expect(wrapper.text()).toContain("Artifacts: 1");
    expect(wrapper.text()).toContain("course_data.json");
    expect(wrapper.text()).toContain("SHA256: 12345678...");
    expect(wrapper.text()).toContain("2 KB");
    expect(wrapper.vm.formatDate(release.updated)).not.toBe("Unknown");
    expect(wrapper.vm.formatBytes("invalid")).toBe("0 B");
    wrapper.unmount();
  });

  it("ignores a stale manifest response after the selection changes", async () => {
    const releases = [
      { release_id: "first", manifest_size: 100 },
      { release_id: "second", manifest_size: 100 },
    ];
    const pending = {};
    vi.stubGlobal("fetch", vi.fn().mockImplementation((url) => {
      const match = url.match(/releases\/([^/]+)\/manifest\/$/);
      if (!match) {
        return Promise.resolve({ ok: true, json: async () => ({ success: true, releases }) });
      }
      return new Promise((resolve) => {
        pending[match[1]] = (artifact) => resolve({
          ok: true,
          json: async () => ({
            success: true,
            manifest: { artifacts: { [artifact]: { size_bytes: 1, checksum_sha256: "abcdef0123" } } },
          }),
        });
      });
    }));
    const wrapper = mount(DataReleasePromotion);
    await flushPromises();
    await wrapper.findAll(".list-group-item")[0].trigger("click");
    await wrapper.findAll(".list-group-item")[1].trigger("click");
    pending.second("second-artifact");
    await flushPromises();
    pending.first("first-artifact");
    await flushPromises();

    expect(wrapper.text()).toContain("second-artifact");
    expect(wrapper.text()).not.toContain("first-artifact");
    expect(wrapper.text()).not.toContain("Loading...");
    wrapper.unmount();
  });

  it("ignores a stale manifest error after the selection changes", async () => {
    vi.spyOn(console, "error").mockImplementation(() => {});
    const releases = [
      { release_id: "first", manifest_size: 100 },
      { release_id: "second", manifest_size: 100 },
    ];
    const pending = {};
    vi.stubGlobal("fetch", vi.fn().mockImplementation((url) => {
      const match = url.match(/releases\/([^/]+)\/manifest\/$/);
      if (!match) {
        return Promise.resolve({ ok: true, json: async () => ({ success: true, releases }) });
      }
      return new Promise((resolve, reject) => {
        pending[match[1]] = { resolve, reject };
      });
    }));

    const wrapper = mount(DataReleasePromotion);
    await flushPromises();
    await wrapper.findAll(".list-group-item")[0].trigger("click");
    await wrapper.findAll(".list-group-item")[1].trigger("click");
    pending.first.reject(new Error("stale failure"));
    await flushPromises();
    pending.second.resolve({
      ok: true,
      json: async () => ({
        success: true,
        manifest: { schema_version: "2.0", artifacts: {} },
      }),
    });
    await flushPromises();

    expect(wrapper.text()).toContain("Schema: 2.0");
    expect(wrapper.find('[role="alert"]').exists()).toBe(false);
    expect(wrapper.text()).not.toContain("Loading...");
    wrapper.unmount();
  });

  it("acknowledges the promoted release even if the selection changes", async () => {
    const releases = [
      { release_id: "first", manifest_size: 100 },
      { release_id: "second", manifest_size: 100 },
    ];
    let resolvePromote;
    const fetch = vi.fn().mockImplementation((url) => {
      if (url.endsWith("/promote/")) {
        return new Promise((resolve) => { resolvePromote = resolve; });
      }
      return Promise.resolve({
        ok: true,
        json: async () => url.endsWith("/manifest/")
          ? { success: true, manifest: { artifacts: {} } }
          : { success: true, releases },
      });
    });
    vi.stubGlobal("fetch", fetch);
    vi.spyOn(window, "confirm").mockReturnValue(true);
    vi.spyOn(window, "setTimeout").mockImplementation(() => 0);

    const wrapper = mount(DataReleasePromotion);
    await flushPromises();
    await wrapper.findAll(".list-group-item")[0].trigger("click");
    await flushPromises();
    await wrapper.findAll("button").find((button) => button.text() === "Promote Release").trigger("click");
    await wrapper.findAll(".list-group-item")[1].trigger("click");
    await flushPromises();
    resolvePromote({
      ok: true,
      json: async () => ({ success: true, data: { release_id: "first", queue_attempt_id: 7 } }),
    });
    await flushPromises();

    const promoteCall = fetch.mock.calls.find(([url]) => url.endsWith("/promote/"));
    expect(JSON.parse(promoteCall[1].body).release_id).toBe("first");
    expect(wrapper.text()).toContain('Release "first" has been queued for import.');
    expect(wrapper.text()).not.toContain('Release "second" has been queued');
    wrapper.unmount();
  });

  it("does not submit a promotion when confirmation is cancelled", async () => {
    const release = { release_id: "release-001", manifest_size: 100 };
    const fetch = vi.fn().mockImplementation((url) => Promise.resolve({
      ok: true,
      json: async () => url.endsWith("/manifest/")
        ? { success: true, manifest: { artifacts: {} } }
        : { success: true, releases: [release] },
    }));
    vi.stubGlobal("fetch", fetch);
    vi.spyOn(window, "confirm").mockReturnValue(false);

    const wrapper = mount(DataReleasePromotion);
    await flushPromises();
    await wrapper.vm.promoteRelease();
    expect(wrapper.find('[role="alert"]').text()).toContain("No release selected");
    await wrapper.find('[aria-label="Dismiss error"]').trigger("click");

    await wrapper.find(".list-group-item").trigger("click");
    await flushPromises();
    await wrapper.findAll("button").find((button) =>
      button.text() === "Promote Release",
    ).trigger("click");

    expect(window.confirm).toHaveBeenCalled();
    expect(fetch.mock.calls.some(([url]) => url.endsWith("/promote/"))).toBe(false);
    wrapper.unmount();
  });

  it("sends the decoded CSRF token and reports promotion failures", async () => {
    vi.spyOn(console, "error").mockImplementation(() => {});
    document.cookie = "csrftoken=csrf%2Fvalue; path=/";
    const release = { release_id: "release-001", manifest_size: 100 };
    const fetch = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, releases: [release] }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, manifest: { artifacts: {} } }),
      })
      .mockResolvedValueOnce({
        ok: false,
        status: 502,
        json: async () => { throw new Error("invalid JSON"); },
      });
    vi.stubGlobal("fetch", fetch);
    vi.spyOn(window, "confirm").mockReturnValue(true);

    const wrapper = mount(DataReleasePromotion);
    await flushPromises();
    await wrapper.find(".list-group-item").trigger("click");
    await flushPromises();
    await wrapper.findAll("button").find((button) =>
      button.text() === "Promote Release",
    ).trigger("click");
    await flushPromises();

    const promoteCall = fetch.mock.calls.find(([url]) => url.endsWith("/promote/"));
    expect(promoteCall[1].headers["X-CSRFToken"]).toBe("csrf/value");
    expect(wrapper.find('[role="alert"]').text()).toContain(
      "Failed to promote release: HTTP 502",
    );
    expect(wrapper.find(".btn-primary").element.disabled).toBe(false);
    wrapper.unmount();
    document.cookie = "csrftoken=; max-age=0; path=/";
  });

  it("shows a promotion API error response", async () => {
    const release = { release_id: "release-001", manifest_size: 100 };
    const fetch = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, releases: [release] }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, manifest: { artifacts: {} } }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: false }),
      });
    vi.stubGlobal("fetch", fetch);
    vi.spyOn(window, "confirm").mockReturnValue(true);

    const wrapper = mount(DataReleasePromotion);
    await flushPromises();
    await wrapper.find(".list-group-item").trigger("click");
    await flushPromises();
    await wrapper.findAll("button").find((button) =>
      button.text() === "Promote Release",
    ).trigger("click");
    await flushPromises();

    expect(wrapper.find('[role="alert"]').text()).toContain("Failed to promote release");
    wrapper.unmount();
  });

  it("returns the date string if locale formatting fails", () => {
    vi.spyOn(Date.prototype, "toLocaleString").mockImplementation(() => {
      throw new Error("locale unavailable");
    });

    expect(DataReleasePromotion.methods.formatDate("not-a-date")).toBe("not-a-date");
  });

  it.each([true, false])("displays the correct promotion result with mock=%s", async (mock) => {
    const release = { release_id: "release-001", manifest_size: 100, updated: null };
    const response = (data) => Promise.resolve({ ok: true, json: async () => data });
    const fetch = vi.fn()
      .mockImplementationOnce(() => response({ success: true, releases: [release], mock }))
      .mockImplementationOnce(() => response({ success: true, manifest: { artifacts: {} } }))
      .mockImplementationOnce(() => response({
        success: true,
        data: mock
          ? { mock: true, message: "Local simulation only; no release was queued or imported." }
          : { queue_attempt_id: 42 },
      }));
    vi.stubGlobal("fetch", fetch);
    vi.spyOn(window, "confirm").mockReturnValue(true);
    vi.spyOn(window, "setTimeout").mockImplementation(() => 0);

    const wrapper = mount(DataReleasePromotion);
    await flushPromises();
    expect(wrapper.text().includes("Local sample data")).toBe(mock);
    await wrapper.find(".list-group-item").trigger("click");
    await flushPromises();
    const promote = wrapper.findAll("button").find((button) => button.text() === "Promote Release");
    await promote.trigger("click");
    await flushPromises();

    expect(window.confirm).toHaveBeenCalledWith(expect.stringContaining(
      mock ? "local simulation" : "queue the data",
    ));
    expect(wrapper.text()).toContain(mock ? "Local simulation only" : "Queue attempt: 42");
    expect(fetch).toHaveBeenCalledTimes(3);
    await wrapper.find('[aria-label="Dismiss success message"]').trigger("click");
    expect(wrapper.find('[role="alert"]').exists()).toBe(false);
    wrapper.unmount();
  });
});
