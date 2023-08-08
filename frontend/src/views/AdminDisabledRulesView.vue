<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { apiGet, showError } from "@/api";
import type { APIError, Rule } from "@/api/types";
import { CAlert, CSpinner } from "@coreui/bootstrap-vue";
import { useQuery } from "vue-query";
import AdminDisabledRulesList from "../components/AdminDisabledRulesList.vue";
import AdminSubHeader from "../components/AdminSubHeader.vue";

const url = `/api/v1/admin/rules`;
const { isLoading, isError, data, error } = useQuery<Rule[], APIError>(
  [url, { disabled: true }],
  apiGet,
  { retry: false },
);
</script>

<template>
  <div v-if="isLoading" class="text-center">
    <CSpinner />
  </div>
  <CAlert v-else-if="isError" color="danger">
    {{ showError(error) }}
  </CAlert>
  <template v-else-if="data">
    <AdminSubHeader />
    <AdminDisabledRulesList :rules="data" />
  </template>
</template>
