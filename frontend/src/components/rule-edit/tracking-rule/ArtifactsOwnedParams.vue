<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { useUserStore } from "@/stores/user";
import UserMultiSelect from "./UserMultiSelect.vue";
const userStore = useUserStore();
const username = userStore.username;
</script>

<template>
  <UserMultiSelect
    label="Artifacts owned by:"
    placeholder="Search by FAS Username"
    nooptionstext="No matches on that username found"
    showArtifactsOwnedSummary
    :initialValue="username ? [username] : undefined"
  />
</template>
