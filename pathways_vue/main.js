import Vue from 'vue';
import VueGtag from "vue-gtag";
import VueMq from 'vue-mq';

import {library} from '@fortawesome/fontawesome-svg-core';
import {
  FontAwesomeIcon,
  FontAwesomeLayers,
  FontAwesomeLayersText,
} from '@fortawesome/vue-fontawesome';

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

// fontaweome
import {
  faUser,
  faLink,
  faEnvelope,
  faSearch,
  faSignOutAlt,
  faHome,
  faPaw,
  faBookmark,
  faExclamationTriangle,
  faGraduationCap,
  faBars,
  faLocationArrow,
  faSquareFull,
  faCaretRight,
  faCaretDown,
  faCaretUp,
  faSquare as fasSquare,
  faTimes,
  faPencilAlt,
  faCheck,
  faPlus,
  faCheckCircle,
  faChevronRight,
  faChevronUp,
  faInfoCircle,
} from '@fortawesome/free-solid-svg-icons';

import {
  faEdit,
  faCreditCard,
  faCalendarAlt,
  faCalendarCheck,
  faSquare,
  faCircle,
} from '@fortawesome/free-regular-svg-icons';

library.add(faUser);
library.add(faLink);
library.add(faEnvelope);
library.add(faSearch);
library.add(faSignOutAlt);
library.add(faHome);
library.add(faPaw);
library.add(faGraduationCap);
library.add(faEdit);
library.add(faCreditCard);
library.add(faCalendarAlt);
library.add(faCalendarCheck);
library.add(faBookmark);
library.add(faExclamationTriangle);
library.add(faInfoCircle);
library.add(faSquare);
library.add(faSquareFull);
library.add(fasSquare);
library.add(faBars);
library.add(faLocationArrow);
library.add(faCaretRight);
library.add(faCaretDown);
library.add(faCaretUp);
library.add(faTimes);
library.add(faPencilAlt);
library.add(faCheck);
library.add(faPlus);
library.add(faCheckCircle);
library.add(faCircle);
library.add(faChevronRight);
library.add(faChevronUp);

// fontawesome 5
Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.component('font-awesome-layers', FontAwesomeLayers);
Vue.component('font-awesome-layers-text', FontAwesomeLayersText);

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
