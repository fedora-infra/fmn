<script setup lang="ts">
import { apiGet } from "@/api";
import type { QueryFunction } from "react-query/types/core";
import { useQuery } from "vue-query";

// const props = defineProps<{ value: string | null }>();

const route = "/api/v1/applications";
const { isLoading, isError, data, error } = useQuery(
  route,
  apiGet as QueryFunction<string[]>
);
</script>

<template>
  <p class="mb-0 fw-bold">Applications:</p>
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
    v-else
    type="multiselect"
    name="applications"
    placeholder="Choose one or more applications"
    mode="tags"
    :msOptions="data"
    searchable
    :close-on-select="false"
  />
</template>
