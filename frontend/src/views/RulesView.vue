<script setup lang="ts">
import { useRulesQuery } from "@/api/rules";
import { CAlert, CSpinner } from "@coreui/bootstrap-vue";
import RulesList from "../components/RulesList.vue";

// Getting rules
const { isLoading, isError, data, error } = useRulesQuery();
console.log(data.value);
</script>

<template>
  <div class="rules">
    <h1>My Rules</h1>
    <div v-if="isLoading" class="text-center"><CSpinner /></div>
    <CAlert v-else-if="isError" color="danger"
      >Could not load the rules: {{ error }}</CAlert
    >
    <RulesList v-else-if="data" :rules="data" />
  </div>
</template>
