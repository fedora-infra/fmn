<script setup lang="ts">
import { CContainer, CNavbar, CNavbarNav } from "@coreui/bootstrap-vue";
import { useI18n } from "vue-i18n";
import { useUserStore } from "../stores/user";
import LoginButton from "./LoginButton.vue";
import MainNavLink from "./MainNavLink.vue";
const userStore = useUserStore();
const { t } = useI18n();
</script>

<template>
  <CNavbar
    expand="lg"
    color-scheme="light"
    class="masthead justify-content-between py-2"
  >
    <CContainer>
      <router-link to="/" class="navbar-brand">
        <img src="@/assets/logo.png" alt="FMN logo" height="40" />
      </router-link>
      <CNavbarNav class="align-items-center">
        <MainNavLink to="/rules" v-if="userStore.loggedIn">{{
          t("rules")
        }}</MainNavLink>
        <LoginButton />
      </CNavbarNav>
    </CContainer>
  </CNavbar>
</template>

<i18n lang="yaml">
en-US:
  rules: "Rules"
fr-FR:
  rules: "Règles"
</i18n>
