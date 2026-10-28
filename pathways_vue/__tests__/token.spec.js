import { createPinia, setActivePinia } from "pinia";
import { afterEach, beforeEach, describe, expect, it } from "vitest";

import { useTokenStore } from "@/stores/token";

const addCsrfInput = (value) => {
  const input = document.createElement("input");
  input.name = "csrfmiddlewaretoken";
  input.value = value;
  document.body.appendChild(input);
  return input;
};

describe("token store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  afterEach(() => {
    const inputs = document.getElementsByName("csrfmiddlewaretoken");
    while (inputs.length) inputs[0].remove();
  });

  it("reads the CSRF token from the hidden input on initialization", () => {
    addCsrfInput("abc123");
    const store = useTokenStore();
    expect(store.csrfToken).toBe("abc123");
  });

  it("has the expected default name", () => {
    addCsrfInput("abc123");
    const store = useTokenStore();
    expect(store.name).toBe("Vue");
  });

  it("exposes a reactive, writable csrfToken", () => {
    addCsrfInput("abc123");
    const store = useTokenStore();
    store.csrfToken = "updated-token";
    expect(store.csrfToken).toBe("updated-token");
  });
});
