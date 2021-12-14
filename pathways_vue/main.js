import { createApp } from 'vue'
import App from './app.vue';
import router from './router';
import store from './store';

import VueGtag from 'vue-gtag-next';
import VueMq from 'vue3-mq';
import axios from 'axios';
import VueAxios from 'vue-axios';
import mitt from 'mitt';

// bootstrap js
import 'bootstrap';

// custom bootstrap theming
import './css/custom.scss';

const app = createApp(App);

// MARK: google analytics data stream measurement_id
const gaCode = document.body.getAttribute('google-analytics');
const debugMode = document.body.getAttribute('django-debug');

const emitter = mitt()
app.config.globalProperties.emitter = emitter;

app.config.productionTip = false;

// vue-gtag
app.use(VueGtag, {
  isEnabled: debugMode == 'false',
  property: {
    id: gaCode,
    params: {
      anonymize_ip: true,
    },
  }
});

// vue-mq (media queries)
app.use(VueMq, {
  breakpoints: {
    // breakpoints == min-widths of next size
    mobile: 768, // tablet begins 768px
    tablet: 992, // desktop begins 992px
    desktop: Infinity,
  },
});
app.use(router);
app.use(store);
app.use(VueAxios, axios);

app.mount("#app");
