import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("@/composables/customFetch", () => ({ useCustomFetch: vi.fn() }));

import { useCustomFetch } from "@/composables/customFetch";
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

  it("pluralizes the heading when there are multiple majors", async () => {
    setContext({
      majors: [
        { major_abbr_code: "CSE", major_premaj: false },
        { major_abbr_code: "MATH", major_premaj: false },
      ],
      intended_majors: [],
    });
    const wrapper = await mountHome();
    expect(wrapper.text()).toContain("Majors");
    expect(wrapper.findAll("h2").map((h) => h.text())).toContain("My Majors");
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

  it("shows no intended majors message when there are none", async () => {
    setContext({
      majors: [{ major_abbr_code: "PSOCS", major_premaj: true }],
      intended_majors: [],
    });
    const wrapper = await mountHome();
    expect(wrapper.text()).toContain("No intended majors found.");
  });

  it("pluralizes the intended majors heading when there are multiple", async () => {
    setContext({
      majors: [{ major_abbr_code: "PSOCS", major_premaj: true }],
      intended_majors: [
        { major_abbr_code: "PHYS" },
        { major_abbr_code: "CHEM" },
      ],
    });
    const wrapper = await mountHome();
    const headings = wrapper.findAll("h2").map((h) => h.text());
    expect(headings).toContain("My Intended Majors");
  });

  it("defaults majors and intended_majors to an empty array when absent", async () => {
    setContext({});
    const wrapper = await mountHome();
    expect(wrapper.vm.majors).toEqual([]);
    expect(wrapper.vm.intendedMajors).toEqual([]);
    expect(wrapper.text()).toContain("No majors found.");
  });

  it("shows the debug-only test display majors section when debugMode is enabled", async () => {
    setContext({ majors: [], intended_majors: [] });
    const wrapper = await mountHome();
    wrapper.vm.contextStore.context.debugMode = true;
    await wrapper.vm.$nextTick();
    expect(wrapper.text()).toContain("Test Display Majors");
  });

  it("shows the preferred first name and debug JSON dump when provided", async () => {
    const el = document.createElement("div");
    el.id = "django-context-data";
    el.textContent = JSON.stringify({
      debugMode: true,
      personData: {
        majors: [],
        intended_majors: [],
        preferred_first_name: "Jamie",
        uwnetid: "jdoe",
        class_desc: "Junior",
      },
    });
    document.body.appendChild(el);
    const wrapper = await mountHome();
    const welcomeHeading = wrapper.findAll("h2")[0];
    expect(welcomeHeading.text()).toContain("Jamie");
    expect(welcomeHeading.text()).not.toContain("jdoe");
    expect(wrapper.text()).toContain("Junior");
    expect(wrapper.text()).toContain('"preferred_first_name": "Jamie"');
  });
});

describe("Home page toPercent calculation", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  afterEach(() => {
    document.getElementById("django-context-data")?.remove();
  });

  it("clamps percentage values between 0 and 100", async () => {
    setContext({ majors: [], intended_majors: [] });
    const wrapper = await mountHome();
    expect(wrapper.vm.toPercent(50, 100)).toBe(50);
    expect(wrapper.vm.toPercent(150, 100)).toBe(100);
    expect(wrapper.vm.toPercent(-10, 100)).toBe(0);
    expect(wrapper.vm.toPercent(undefined, 100)).toBe(0);
    expect(wrapper.vm.toPercent(50, 0)).toBe(0);
  });
});

describe("Home page welcome modal and preference saving", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.restoreAllMocks();
  });

  afterEach(() => {
    document.getElementById("django-context-data")?.remove();
  });

  it("shows the welcome modal", async () => {
    setContext({ majors: [], intended_majors: [] });
    const wrapper = await mountHome();

    const showMock = vi.fn();
    const modalElement = document.createElement("div");
    modalElement.id = "exampleModal";
    document.body.appendChild(modalElement);
    global.Modal = vi.fn(function () {
      this.show = showMock;
    });

    wrapper.vm.showWelcomeModal();

    expect(global.Modal).toHaveBeenCalledWith(modalElement, {});
    expect(showMock).toHaveBeenCalled();

    modalElement.remove();
    delete global.Modal;
  });

  it("saves the welcome display preference successfully", async () => {
    setContext({ majors: [], intended_majors: [] });
    useCustomFetch.mockResolvedValueOnce({});
    const wrapper = await mountHome();

    await wrapper.vm.saveModalPref();

    expect(useCustomFetch).toHaveBeenCalledWith("/api/v1/user_pref/", {
      method: "POST",
      body: JSON.stringify({ viewed_welcome_display: true }),
      headers: { "Content-Type": "application/json" },
    });
  });

  it("logs an error when saving the welcome display preference fails", async () => {
    setContext({ majors: [], intended_majors: [] });
    const error = new Error("network failure");
    useCustomFetch.mockRejectedValueOnce(error);
    const consoleErrorSpy = vi
      .spyOn(console, "error")
      .mockImplementation(() => {});
    const wrapper = await mountHome();

    await wrapper.vm.saveModalPref();

    expect(consoleErrorSpy).toHaveBeenCalledWith(
      "Failed to save welcome display preference:",
      error,
    );
  });
});
