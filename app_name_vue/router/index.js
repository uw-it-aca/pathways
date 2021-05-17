import Vue from 'vue';
import VueRouter from 'vue-router';

// page components
import Home from '../pages/home.vue';
import Customize from '../pages/customize.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/customize/",
    name: "Customize",
    component: Customize,
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
