<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { useDisabledRulesQuery } from "@/api/rules";
import { CAlert, CSpinner } from "@coreui/bootstrap-vue";
import AdminDisabledRulesList from "../components/AdminDisabledRulesList.vue";
import AdminSubHeader from "../components/AdminSubHeader.vue";

const { isLoading, isError, data, error } = useDisabledRulesQuery();
</script>

<template>
  <div v-if="isLoading" class="text-center">
    <CSpinner />
  </div>
  <CAlert v-else-if="isError" color="danger">
    {{ error?.detail }}
  </CAlert>
  <template v-else-if="data">
    <AdminSubHeader />
    <AdminDisabledRulesList :rules="data" />
  </template>
</template>
