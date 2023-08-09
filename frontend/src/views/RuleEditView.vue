<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { apiGet, showError } from "@/api";
import type { APIError, Rule } from "@/api/types";
import { useUserStore } from "@/stores/user";
import { CAlert, CSpinner } from "@coreui/bootstrap-vue";
import { useQuery } from "@tanstack/vue-query";
import { useRoute } from "vue-router";
import RuleEditForm from "../components/RuleEditForm.vue";

const route = useRoute();
const userStore = useUserStore();

const url = `/api/v1/users/${userStore.username}/rules/${route.params.id}`;
const { isLoading, isError, data, error } = useQuery<Rule, APIError>(
  [url],
  apiGet,
);
</script>

<template>
  <div v-if="isLoading" class="text-center"><CSpinner /></div>
  <CAlert v-else-if="isError" color="danger">
    Could not load the rule: {{ showError(error) }}
  </CAlert>
  <RuleEditForm v-else-if="data" :rule="data" />
</template>
