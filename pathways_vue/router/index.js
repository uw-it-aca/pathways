import { createWebHistory, createRouter } from "vue-router";

// page components
import Home from '../pages/home.vue';
import Course from '../pages/course.vue';
import Major from '../pages/major.vue';

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/course",
    name: "Course",
    component: Course,
    pathToRegexpOptions: { strict: true }
  },
  {
    path: "/major",
    name: "Major",
    component: Major,
    pathToRegexpOptions: { strict: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
