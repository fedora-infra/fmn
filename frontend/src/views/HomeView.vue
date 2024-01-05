<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { useRulesQuery } from "@/api/rules";
import { CAlert, CSpinner } from "@coreui/bootstrap-vue";
import RulesList from "../components/RulesList.vue";
import { useUserStore } from "../stores/user";

const userStore = useUserStore();

// Getting rules
const { isLoading, isError, data, error } = useRulesQuery();
</script>

<template>
  <template v-if="userStore.username">
    <div class="rules">
      <div v-if="isLoading" class="text-center"><CSpinner /></div>
      <CAlert v-else-if="isError" color="danger"
        >Could not load the rules: {{ error }}</CAlert
      >
      <RulesList v-else-if="data" :rules="data" />
    </div>
  </template>
  <template v-else>
    <div class="p-5 mb-4">
      <div class="home">
        <h1 class="fw-bold display-5">Notifications</h1>
        <p class="col-md-8 fs-4">
          Centrally managed preferences for Fedora Infrastructure notifications
          to your inbox, chat client, and mobile device.
        </p>
      </div>
    </div>
  </template>
</template>

<style></style>
