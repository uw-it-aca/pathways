import { createApp } from 'vue'
import App from './app.vue';
import router from './router';
import store from './store';

import VueGtag from 'vue-gtag-next';
import VueMq from 'vue3-mq';

// bootstrap js
import 'bootstrap';

// custom theming and global styles
import './css/custom.scss';
import './css/global.scss';

const app = createApp(App);

// MARK: google analytics data stream measurement_id
const gaCode = document.body.getAttribute('google-analytics');
const debugMode = document.body.getAttribute('django-debug');

app.config.productionTip = false;

// vue-gtag
app.use(VueGtag, {
  config: {
    id: gaCode,
    params: {
      anonymize_ip: true,
    },
  },
  enabled: debugMode == 'true',
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

app.mount("#app");
