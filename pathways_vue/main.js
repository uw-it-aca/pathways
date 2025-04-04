import { createApp } from "vue";

import VueGtag from "vue-gtag-next";
import { Vue3Mq, MqResponsive } from "vue3-mq";
//import axios from "axios";
//import VueAxios from "vue-axios";
import mitt from "mitt";

// bootstrap js + bootstrap-icons
import "bootstrap";
import "bootstrap-icons/font/bootstrap-icons.css";

// solstice bootstrap theme
import "solstice-theme/dist/solstice.scss";

// solstice-vue comps
import "solstice-vue/dist/style.css";

// bootstrap-vue-next css
import "bootstrap-vue-next/dist/bootstrap-vue-next.css";

const app = createApp(App);

// google analytics data stream measurement and user hashed ids
const gaCode = document.body.getAttribute("data-google-analytics");
const debugMode = document.body.getAttribute("data-django-debug");
const hashedId = window.hashed_netid;

app.config.productionTip = false;

// mitt
const emitter = mitt();
app.config.globalProperties.emitter = emitter;

// vue-gtag-next
app.use(VueGtag, {
  isEnabled: debugMode == "false",
  property: {
    id: gaCode,
    params: {
      anonymize_ip: true,
      user_id: hashedId,
    },
  },
});

// vue-mq (media queries)
app.use(Vue3Mq, {
  preset: "bootstrap5",
});
app.component(MqResponsive);

// vue-axios
//app.use(VueAxios, axios);

// solstice-vue
app.use(SolsticeVue);

// vue-router
app.use(router);

app.mount("#app");
