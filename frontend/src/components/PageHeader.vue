<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { CContainer, CNavbar, CNavbarNav } from "@coreui/bootstrap-vue";
import LoginButton from "./LoginButton.vue";
import AdminLink from "./AdminLink.vue";
</script>

<template>
  <CNavbar
    expand="lg"
    color-scheme="light"
    class="masthead justify-content-between py-2 mb-5"
  >
    <CContainer>
      <router-link to="/" class="navbar-brand">
        <img src="@/assets/logo.png" alt="FMN logo" height="40" />
      </router-link>
      <CNavbarNav class="align-items-center">
        <AdminLink />
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
