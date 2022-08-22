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
      path: "/rules",
      name: "rules",
      component: () => import("../views/RulesView.vue"),
      meta: { auth: true },
    },
    {
      path: "/rules/new",
      name: "new-rule",
      component: () => import("../views/NewRuleView.vue"),
      meta: { auth: true },
    },
  ],
});

export default router;
