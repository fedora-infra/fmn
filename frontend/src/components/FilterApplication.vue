<script setup lang="ts">
import type { QueryFunction } from "react-query/types/core";
import { useQuery } from "vue-query";
import { apiGet } from "../api";

// const props = defineProps<{ value: string | null }>();

const route = "/applications";
const { isLoading, isError, data, error } = useQuery(
  route,
  apiGet as QueryFunction<string[]>
);
</script>

<template>
  <p class="mb-0">Only notify for the selected applications:</p>
  <p v-if="isLoading">
    <input
      type="text"
      class="form-control"
      disabled
      value="Loading applications..."
    />
  </p>
  <p v-else-if="isError">Error: {{ error }}</p>
  <FormKit
    type="multiselect"
    name="applications"
    placeholder="Select applications"
    mode="tags"
    :msOptions="data"
    searchable
    :close-on-select="false"
  />
</template>
