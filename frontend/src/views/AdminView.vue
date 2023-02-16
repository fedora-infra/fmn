<script setup lang="ts">
import { useDisabledRulesQuery } from "@/api/rules";
import { CAlert, CSpinner } from "@coreui/bootstrap-vue";
import AdminRulesList from "../components/AdminRulesList.vue";

const { isLoading, isError, data, error } = useDisabledRulesQuery();
</script>

<template>
  <div v-if="isLoading" class="text-center">
    <CSpinner />
  </div>
  <CAlert v-else-if="isError" color="danger">{{ error }}</CAlert>
  <template v-else-if="data">
    <h1 class="border-bottom mb-5 pb-2">Admin Dashboard</h1>
    <AdminRulesList :rules="data" />
  </template>
</template>
