// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import type { Destination } from "@/api/types";
import { vctooltip } from "@coreui/bootstrap-vue";
import { render as baseRender } from "@testing-library/vue";
import { getActivePinia, type Pinia } from "pinia";
import { vi } from "vitest";
import type { Component } from "vue";
import { createI18n } from "vue-i18n";
import router from "../router";
import type { useUserStore } from "../stores/user";

export const loginUser = (userStore: ReturnType<typeof useUserStore>) => {
  userStore.$patch({
    accessToken: "testing",
    username: "dummy-user",
    fullName: "Dummy User",
    email: "dummy@example.com",
  });
};

export const loginAdmin = (userStore: ReturnType<typeof useUserStore>) => {
  userStore.$patch({
    accessToken: "testing",
    username: "admin-user",
    fullName: "Admin User",
    email: "admin@example.com",
    isAdmin: true,
  });
};

export const render = (
  component: Component,
  props?: Record<string, boolean | Destination>,
) => {
  const pinia = getActivePinia() as Pinia;
  const i18n = createI18n({
    legacy: false,
    locale: navigator.language,
    fallbackLocale: "en-US",
    messages: {},
  });
  return baseRender(component, {
    props: props,
    global: {
      plugins: [router, pinia, i18n],
      provide: {
        auth: vi.fn(),
        icons: {},
      },
      directives: {
        "c-tooltip": vctooltip,
      },
    },
  });
};
