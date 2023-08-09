// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { vueQueryPluginOptions } from "@/api";
import type { UserInfoResponseJson } from "@/auth/userinfo_request";
import { config as formkitConfig } from "@/forms/index";
import { plugin as FormKitPlugin } from "@formkit/vue";
import { VueQueryPlugin } from "@tanstack/vue-query";
import type { RenderOptions } from "@testing-library/vue";
import { getActivePinia, type Pinia } from "pinia";
import { vi } from "vitest";
import { createI18n } from "vue-i18n";
import router from "../router";

export const getRenderOptions = (): RenderOptions => {
  const pinia = getActivePinia() as Pinia;
  const i18n = createI18n({
    legacy: false,
    locale: navigator.language,
    fallbackLocale: "en-US",
    messages: {},
  });
  return {
    global: {
      plugins: [
        router,
        pinia,
        i18n,
        [FormKitPlugin, formkitConfig],
        [VueQueryPlugin, vueQueryPluginOptions],
      ],
      provide: {
        auth: {
          fetchServiceConfiguration: vi.fn().mockResolvedValue(null),
          handleAuthorizationRedirect: vi.fn().mockResolvedValue(null),
          makeUserInfoRequest: vi
            .fn()
            .mockResolvedValue({} as UserInfoResponseJson),
        },
      },
    },
  };
};
