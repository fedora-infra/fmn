<script setup lang="ts">
import { apiGet } from "@/api";
import type { Rule } from "@/api/types";
import { useUserStore } from "@/stores/user";
import { CAlert, CSpinner } from "@coreui/bootstrap-vue";
import type { QueryFunction } from "react-query/types/core";
import { useQuery } from "vue-query";
import { useRoute } from "vue-router";
import RuleEditForm from "../components/RuleEditForm.vue";

const route = useRoute();
const userStore = useUserStore();

const url = `/user/${userStore.username}/rules/${route.params.id}`;
const { isLoading, isError, data, error } = useQuery(
  url,
  apiGet as QueryFunction<Rule>
);
</script>

<template>
  <div v-if="isLoading" class="text-center"><CSpinner /></div>
  <CAlert v-else-if="isError" color="danger"
    >Could not load the rule: {{ error }}</CAlert
  >
  <RuleEditForm v-else-if="data" :rule="data" />
</template>
