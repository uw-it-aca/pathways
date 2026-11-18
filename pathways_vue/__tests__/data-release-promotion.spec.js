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
    wrapper.unmount();
  });
});
