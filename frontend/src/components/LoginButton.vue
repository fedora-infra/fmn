<template>
  <CDropdown v-if="userStore.loggedIn" variant="nav-item" alignment="end">
    <CDropdownToggle component="a">
      <img :alt="userStore.user.username!" :src="avatarURL" />
    </CDropdownToggle>
    <CDropdownMenu>
      <CDropdownItem @click="doLogout()">{{ t("logout") }}</CDropdownItem>
    </CDropdownMenu>
  </CDropdown>
  <CNavItem v-else>
    <CButton @click.prevent="doLogin()" component="a" color="primary">
      {{ t("login") }}
    </CButton>
  </CNavItem>
</template>

<script setup lang="ts">
import {
  CButton,
  CDropdown,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
  CNavItem,
} from "@coreui/bootstrap-vue";
import { useI18n } from "vue-i18n";
import { useRoute, useRouter } from "vue-router";
import { login, logout, useAuth } from "../auth";
import { useUserStore } from "../stores/user";
import { generateLibravatarURL } from "../util";

const auth = useAuth();
const route = useRoute();
const userStore = useUserStore();
const router = useRouter();
const { t } = useI18n();

const avatarURL = generateLibravatarURL(userStore.email, 30, "retro");

const doLogin = () => login(auth, route.fullPath);

const doLogout = () => {
  logout();
  if (route.meta.auth) {
    router.push("/");
  }
};
</script>

<i18n lang="yaml">
en-US:
  login: "Login"
  logout: "Logout"
fr-FR:
  login: "Connexion"
  logout: "Déconnexion"
</i18n>
