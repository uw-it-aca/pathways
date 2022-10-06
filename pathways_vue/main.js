import { createApp } from "vue";
import App from "./app.vue";
import router from "./router";

import VueGtag from "vue-gtag";

import { Vue3Mq, MqResponsive } from "vue3-mq";

import axios from "axios";
import VueAxios from "vue-axios";
import mitt from "mitt";

// bootstrap js
import "bootstrap";

// custom bootstrap theming
import "./css/custom.scss";

const app = createApp(App);

// MARK: google analytics data stream measurement_id
const gaCode = document.body.getAttribute("data-google-analytics");
const debugMode = document.body.getAttribute("data-django-debug");

app.config.productionTip = false;

// mitt
const emitter = mitt();
app.config.globalProperties.emitter = emitter;

// vue-gtag (w/ vue-router auto-tracking)
app.use(
  VueGtag,
  {
    isEnabled: debugMode == "false",
    property: {
      id: gaCode,
      params: {
        anonymize_ip: true,
      },
    },
  },
  router
);

// vue-mq (media queries)
app.use(Vue3Mq, {
  preset: "bootstrap5",
});
app.component("mq-responsive", MqResponsive);

// vue-axios
app.use(VueAxios, axios);
// vue-router
app.use(router);

app.mount("#app");
