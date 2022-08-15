<script setup lang="ts">
import {
  CNavbar,
  CContainer,
  CNavbarBrand,
  CNavbarNav,
} from "@coreui/bootstrap-vue";
import LoginButton from "./LoginButton.vue";
import MainNavLink from "./MainNavLink.vue";
import { useUserStore } from "../stores/user";
const userStore = useUserStore();
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
        <MainNavLink to="/">Home</MainNavLink>
        <MainNavLink to="/about">About</MainNavLink>
        <MainNavLink to="/rules" v-if="userStore.loggedIn">Rules</MainNavLink>
        <MainNavLink to="/destinations" v-if="userStore.loggedIn"
          >Destinations</MainNavLink
        >
        <LoginButton />
      </CNavbarNav>
    </CContainer>
  </CNavbar>
</template>
