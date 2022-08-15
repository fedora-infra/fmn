<script setup lang="ts">
import {
  CNavbar,
  CContainer,
  CNavbarBrand,
  CNavbarNav,
} from "@coreui/bootstrap-vue";
import LoginButton from "./LoginButton.vue";
import MainNavLink from "./MainNavLink.vue";
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
        <MainNavLink to="/rules">Rules</MainNavLink>
        <MainNavLink to="/destinations">Destinations</MainNavLink>
        <LoginButton />
      </CNavbarNav>
    </CContainer>
  </CNavbar>
</template>
