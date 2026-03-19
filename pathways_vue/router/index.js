import { createWebHistory, createRouter } from "vue-router";
import { trackRouter } from "vue-gtag-next";

const routes = [
  {
    path: "/",
    component: () => import("@/pages/home.vue"),
  },
  {
    path: "/faq",
    component: () => import("@/pages/faq.vue"),
    pathToRegexpOptions: { strict: true },
  },
  {
    path: "/course",
    component: () => import("@/pages/course.vue"),
    pathToRegexpOptions: { strict: true },
  },
  {
    path: "/major",
    component: () => import("@/pages/major.vue"),
    pathToRegexpOptions: { strict: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// add router tracking to vue-gtag-next
trackRouter(router);

export default router;
