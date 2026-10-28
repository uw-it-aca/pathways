import { createPinia, setActivePinia } from "pinia";
import { afterEach, beforeEach, describe, expect, it } from "vitest";

import { useContextStore } from "@/stores/context";

const setContextData = (data) => {
  const el = document.createElement("div");
  el.id = "django-context-data";
  el.textContent = JSON.stringify(data);
  document.body.appendChild(el);
  return el;
};

describe("context store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  afterEach(() => {
    document.getElementById("django-context-data")?.remove();
  });

  it("parses the Django context JSON from the DOM on initialization", () => {
    setContextData({ user: "jdoe", loginUser: "jdoe", campus: "Seattle" });
    const store = useContextStore();
    expect(store.context).toEqual({
      user: "jdoe",
      loginUser: "jdoe",
      campus: "Seattle",
    });
  });

  it("has the expected default name", () => {
    setContextData({});
    const store = useContextStore();
    expect(store.name).toBe("Context");
  });

  it("handles an empty context object", () => {
    setContextData({});
    const store = useContextStore();
    expect(store.context).toEqual({});
  });

  it("exposes a reactive, writable context", () => {
    setContextData({ user: "jdoe" });
    const store = useContextStore();
    store.context = { user: "asmith" };
    expect(store.context.user).toBe("asmith");
  });
});
