import { defineStore } from "pinia";

export const useTokenStore = defineStore("token", {
  // id is required so that Pinia can connect the store to the devtools
  state: () => {
    return {
      name: "Vue",
      csrfToken: document.getElementsByName("csrfmiddlewaretoken")[0].value,
    };
  },
  getters: {},
  actions: {},
});
