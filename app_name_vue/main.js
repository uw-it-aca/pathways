import Vue from 'vue';
import VueGtag from "vue-gtag";
import VueMq from 'vue-mq';
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue';

import App from "./app.vue";
import router from "./router";
import store from "./store";

// custom theming and global styles
import './css/custom.scss';
import './css/global.scss';

// MARK: google analytics data stream measurement_id
const gaCode = document.body.getAttribute('google-analytics');
const debugMode = document.body.getAttribute('django-debug');

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

// vue-gtag
Vue.use(VueGtag, {
  config: {
    id: gaCode,
    params: {
      anonymize_ip: true,
    },
  },
  enabled: debugMode == 'true',
});

Vue.use(VueMq, {
  breakpoints: {
    // default mobile is 320px - 767px
    mobile: 767, // tablet begins 768px
    tablet: 991, // desktop begins 992px
    desktop: Infinity,
  }
});

Vue.config.devtools = process.env.VUE_DEVTOOLS === "True";

export const dataBus = new Vue();

// vue app will be rendered inside of #main div found in index.html using webpack_loader
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#main");
