import { createWebHistory, createRouter } from "vue-router";

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
    path: "/customize",
    name: "Customize",
    component: Customize,
    pathToRegexpOptions: { strict: true }
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
