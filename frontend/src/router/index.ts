// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

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
      path: "/rules/new",
      name: "new-rule",
      component: () => import("../views/NewRuleView.vue"),
      meta: { auth: true },
    },
    {
      path: "/rules/:id",
      name: "rule-edit",
      component: () => import("../views/RuleEditView.vue"),
      meta: { auth: true },
    },
    {
      path: "/admin/",
      redirect: "/admin/disabled-rules",
    },
    {
      path: "/admin/disabled-rules",
      name: "admin-disabled-rules",
      component: () => import("../views/AdminDisabledRulesView.vue"),
      meta: { auth: true },
    },
    {
      path: "/admin/user-rules",
      name: "admin-user-rules",
      component: () => import("../views/AdminUserRulesView.vue"),
      meta: { auth: true },
    },
    // will match everything and put it under `$route.params.pathMatch`
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: () => import("../views/NotFoundView.vue"),
    },
  ],
  scrollBehavior: (to, from, savedPosition) => {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { left: 0, top: 0 };
    }
  },
});

export default router;
