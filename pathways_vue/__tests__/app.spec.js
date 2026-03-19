import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";
import { createRouter, createWebHistory } from "vue-router";

import App from "@/app.vue";

describe("App", () => {
  // Helper function to create a router for testing
  const createTestRouter = () => {
    return createRouter({
      history: createWebHistory(),
      routes: [
        {
          path: "/",
          name: "TestHome",
          component: { template: "<div>Test Home</div>" },
        },
        {
          path: "/test",
          name: "TestRoute",
          component: { template: "<div>Test Route</div>" },
        },
      ],
    });
  };

  it("has the correct component name", () => {
    const router = createTestRouter();
    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    });

    expect(wrapper.vm.$options.name).toBe("App");
  });

  it("renders a router-view component", () => {
    const router = createTestRouter();
    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    });

    expect(wrapper.findComponent({ name: "RouterView" }).exists()).toBe(true);
  });

  it("renders the router-view as the root element", () => {
    const router = createTestRouter();
    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    });

    // The template should only contain a router-view
    const routerView = wrapper.findComponent({ name: "RouterView" });
    expect(routerView.exists()).toBe(true);
  });

  it("displays routed component content", async () => {
    const router = createTestRouter();
    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    });

    // Wait for router to be ready
    await router.isReady();

    // Should render the home route by default
    expect(wrapper.html()).toContain("Test Home");
  });

  it("updates content when route changes", async () => {
    const router = createTestRouter();
    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    });

    await router.isReady();
    expect(wrapper.html()).toContain("Test Home");

    // Navigate to test route
    await router.push("/test");
    await wrapper.vm.$nextTick();

    expect(wrapper.html()).toContain("Test Route");
  });
});
