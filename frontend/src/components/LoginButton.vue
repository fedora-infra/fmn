<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<template>
  <template v-if="showButton">
    <CDropdown v-if="userStore.loggedIn" variant="nav-item" alignment="end">
      <CDropdownToggle component="a">
        <img :alt="userStore.user.username!" :src="avatarURL" />
      </CDropdownToggle>
      <CDropdownMenu>
        <CDropdownItem @click="() => router.push('/')">
          {{ t("My rules") }}
        </CDropdownItem>
        <CDropdownItem @click="doLogout()">{{ t("logout") }}</CDropdownItem>
      </CDropdownMenu>
    </CDropdown>
    <CNavItem v-else>
      <CButton
        @click.prevent="doLogin()"
        component="a"
        color="primary"
        :disabled="loading"
      >
        {{ t("login") }}
        <CSpinner v-if="loading" size="sm" class="ms-1" />
      </CButton>
    </CNavItem>
  </template>
</template>

<script setup lang="ts">
import {
  CButton,
  CDropdown,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
  CNavItem,
  CSpinner,
} from "@coreui/bootstrap-vue";
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { login, logout, useAuth } from "../auth";
import { useUserStore } from "../stores/user";
import { generateLibravatarURL } from "../util";

const auth = useAuth();
const userStore = useUserStore();
const router = useRouter();
const { t } = useI18n();

const avatarURL = computed(() =>
  generateLibravatarURL(userStore.email, 30, "retro"),
);

const loading = ref(false);

const doLogin = async () => {
  loading.value = true;
  try {
    await login(auth, router.currentRoute.value.fullPath);
  } catch (err) {
    loading.value = false;
  }
};

const doLogout = () => {
  logout();
  if (router.currentRoute.value.meta.auth) {
    router.push("/");
  }
};

const showButton = computed(() => {
  return (
    // Wait for the initial routing to have happened
    router.currentRoute.value.matched.length > 0 &&
    // Don't show the button on the login callbacks (only Fedora OIDC for now)
    router.currentRoute.value.path.slice(0, 7) !== "/login/"
  );
});
</script>

<i18n lang="yaml">
en-US:
  login: "Login"
  logout: "Logout"
fr-FR:
  login: "Connexion"
  logout: "Déconnexion"
</i18n>
