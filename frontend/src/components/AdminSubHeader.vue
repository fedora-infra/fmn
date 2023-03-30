<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { CNav, CNavItem } from "@coreui/bootstrap-vue";
</script>

<template>
  <h1 class="border-bottom mb-5 pb-2">Admin Dashboard</h1>
  <CNav variant="tabs" class="mb-2">
    <CNavItem>
      <router-link to="/admin/disabled-rules" class="nav-link"
        >Disabled Rules List</router-link
      >
    </CNavItem>
    <CNavItem>
      <router-link to="/admin/user-rules" class="nav-link"
        >User Rules</router-link
      >
    </CNavItem>
  </CNav>
</template>
