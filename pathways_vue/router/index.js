import { createWebHistory, createRouter } from "vue-router";
import { trackRouter } from "vue-gtag-next";

// page components
import Home from "@/pages/home.vue";
import Course from "@/pages/course.vue";
import Major from "@/pages/major.vue";
import Faq from "@/pages/faq.vue";

const routes = [
  {
    path: "/",
    component: Home,
  },
  {
    path: "/faq",
    component: Faq,
    pathToRegexpOptions: { strict: true },
  },
  {
    path: "/course",
    component: Course,
    pathToRegexpOptions: { strict: true },
  },
  {
    path: "/major",
    component: Major,
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
