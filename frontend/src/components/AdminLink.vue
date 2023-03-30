<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();
</script>

<template>
  <router-link v-if="userStore.isAdmin" to="/admin" class="nav-link"
    >Admin</router-link
  >
</template>
