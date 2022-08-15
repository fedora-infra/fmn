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
        <MainNavLink to="/about">{{ t("about") }}</MainNavLink>
        <MainNavLink to="/rules" v-if="userStore.loggedIn">{{
          t("rules")
        }}</MainNavLink>
        <MainNavLink to="/destinations" v-if="userStore.loggedIn">{{
          t("destinations")
        }}</MainNavLink>
        <LoginButton />
      </CNavbarNav>
    </CContainer>
  </CNavbar>
</template>

<i18n lang="yaml">
en-US:
  home: "Home"
  about: "About"
  rules: "Rules"
  destinations: "Destinations"
fr-FR:
  home: "Accueil"
  about: "À propos"
  rules: "Règles"
  destinations: "Destinations"
</i18n>
