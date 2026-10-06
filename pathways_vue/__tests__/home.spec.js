import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("@/composables/customFetch", () => ({ useCustomFetch: vi.fn() }));

import Home from "@/pages/home.vue";

const setContext = (personData) => {
  const el = document.createElement("div");
  el.id = "django-context-data";
  el.textContent = JSON.stringify({ personData });
  document.body.appendChild(el);
};

const mountHome = async () => {
  const wrapper = mount(Home, {
    global: {
      stubs: {
        DefaultLayout: { template: "<div><slot name='content' /></div>" },
        MajorMini: {
          props: ["majorAbbrCode"],
          template: "<div class='major-mini'>{{ majorAbbrCode }}</div>",
        },
        MajorTitle: true,
        SearchMini: true,
        SHeading: { template: "<h2><slot /></h2>" },
        BCard: { template: "<div><slot /></div>" },
        BProgress: true,
      },
    },
  });
  await flushPromises();
  return wrapper;
};

describe("Home page pre-major display", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  afterEach(() => {
    document.getElementById("django-context-data")?.remove();
  });

  it("shows declared majors when none are pre-majors", async () => {
    setContext({
      majors: [{ major_abbr_code: "CSE", major_premaj: false }],
      intended_majors: [{ major_abbr_code: "PHYS" }],
    });
    const wrapper = await mountHome();
    const headings = wrapper.findAll("h2").map((h) => h.text());
    expect(headings).toContain("My Major");
    expect(headings).not.toContain("My Intended Major");
    expect(wrapper.text()).toContain("CSE");
  });

  it("shows intended majors when any declared major is a pre-major", async () => {
    setContext({
      majors: [{ major_abbr_code: "PSOCS", major_premaj: true }],
      intended_majors: [{ major_abbr_code: "PHYS" }],
    });
    const wrapper = await mountHome();
    const headings = wrapper.findAll("h2").map((h) => h.text());
    expect(headings).toContain("My Intended Major");
    expect(headings).not.toContain("My Major");
    const miniText = wrapper
      .findAll(".major-mini")
      .map((m) => m.text());
    expect(miniText).toContain("PHYS");
    expect(miniText).not.toContain("PSOCS");
  });

  it("hasPremajor is false when majors is empty", async () => {
    setContext({ majors: [], intended_majors: [] });
    const wrapper = await mountHome();
    expect(wrapper.vm.hasPremajor).toBe(false);
    expect(wrapper.findAll("h2").map((h) => h.text())).toContain("My Major");
  });
});
