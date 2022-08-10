import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkActiveClass: "active",
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/rules",
      name: "rules",
      component: () => import("../views/RulesView.vue"),
      meta: { auth: true },
    },
    {
      path: "/destinations",
      name: "destinations",
      component: () => import("../views/DestinationsView.vue"),
      meta: { auth: true },
    },
  ],
});

export default router;
