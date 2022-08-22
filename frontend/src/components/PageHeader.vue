<script setup lang="ts">
import {
  CContainer,
  CNavbar,
  CNavbarBrand,
  CNavbarNav,
} from "@coreui/bootstrap-vue";
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
      <CNavbarBrand href="/">
        <img src="@/assets/logo.png" alt="FMN logo" height="40" />
      </CNavbarBrand>
      <CNavbarNav class="align-items-center">
        <MainNavLink to="/">{{ t("home") }}</MainNavLink>
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
  home: "Home"
  rules: "Rules"
fr-FR:
  home: "Accueil"
  rules: "Règles"
</i18n>
