// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { useAuth } from "@/auth";
import type Authenticator from "@/auth/authenticator";
import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import { markRaw } from "vue";
import { useRouter, type Router } from "vue-router";

declare module "pinia" {
  export interface PiniaCustomProperties {
    $router: Router;
    $auth: Authenticator;
  }
}

function addUsefulObjects() {
  const router = useRouter();
  const auth = useAuth();
  return {
    $router: markRaw(router),
    $auth: markRaw(auth),
  };
}

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
pinia.use(addUsefulObjects);

export default pinia;
