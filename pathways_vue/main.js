import { createBootstrap } from "bootstrap-vue-next";
import { createApp } from "vue";
import { createPinia } from "pinia";
import VueGtag from "vue-gtag-next";
import { Vue3Mq, MqResponsive } from "vue3-mq";
import mitt from "mitt";

import App from "@/app.vue";
import router from "@/router";
import { useContextStore } from "@/stores/context";

// bootstrap js + bootstrap-icons
import "bootstrap";
import "bootstrap-icons/font/bootstrap-icons.css";

// solstice bootstrap theme
import "solstice-theme/dist/solstice.scss";

// solstice-vue comps
import "solstice-vue/dist/style.css";

// bootstrap-vue-next css
import "bootstrap-vue-next/dist/bootstrap-vue-next.css";

// microsoft clarity
import Clarity from "@microsoft/clarity";

const app = createApp(App);
app.config.globalProperties.window = window;

// pinia (vuex) state management
const pinia = createPinia();
app.use(pinia);

// get contextStore values
const contextStore = useContextStore();

app.config.productionTip = false;

// mitt
const emitter = mitt();
app.config.globalProperties.emitter = emitter;

// vue-mq (media queries)
app.use(Vue3Mq, {
  preset: "bootstrap5",
});
app.component("mq-responsive", MqResponsive);

// google analytics data stream measurement and user hashed ids
// vue-gtag-next
app.use(VueGtag, {
  isEnabled: contextStore.context.debugMode == false,
  property: {
    id: contextStore.context.googleAnalyticsKey,
    params: {
      anonymize_ip: true,
      user_id: contextStore.context.hashedNetid,
    },
  },
});

// bootstrap-vue-next
app.use(createBootstrap());

// vue-router
app.use(router);

// microsoft clarity
Clarity.init(contextStore.context.clarityProjectId);

app.mount("#app");
