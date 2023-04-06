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
import { computed, onUnmounted, ref } from "vue";
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
  generateLibravatarURL(userStore.email, 30, "retro")
);

const loading = ref(false);
const loadingTimer = ref<number | null>(null);

const doLogin = async () => {
  loading.value = true;
  await login(auth, router.currentRoute.value.fullPath);
  loadingTimer.value = window.setTimeout(() => {
    loading.value = false;
  }, 3000);
};

const doLogout = () => {
  logout();
  if (router.currentRoute.value.meta.auth) {
    router.push("/");
  }
};

onUnmounted(() => {
  loadingTimer.value && window.clearTimeout(loadingTimer.value);
});

const showButton = computed(
  // Don't show the button on the OIDC callback
  () => router.currentRoute.value.path !== "/login/fedora"
);
</script>

<i18n lang="yaml">
en-US:
  login: "Login"
  logout: "Logout"
fr-FR:
  login: "Connexion"
  logout: "Déconnexion"
</i18n>
