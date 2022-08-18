<script setup lang="ts">
import type { QueryFunction } from "react-query/types/core";
import { useQuery } from "vue-query";
import { apiGet } from "../api";
import FilterWithSelect from "./FilterWithSelect.vue";

// const props = defineProps<{ value: string | null }>();

const route = "/applications";
const { isLoading, isError, data, error } = useQuery(
  route,
  apiGet as QueryFunction<string[]>
);
</script>

<template>
  <p class="mb-0">Only notify for the selected application:</p>
  <p v-if="isLoading">Loading...</p>
  <p v-else-if="isError">Error: {{ error }}</p>
  <FilterWithSelect v-else name="application" :options="data || []" />
</template>
