<script setup lang="ts">
import { apiGet } from "@/api";
import type { QueryFunction } from "react-query/types/core";

// const props = defineProps<{ value: string | null }>();

const apiGetApplications = apiGet as QueryFunction<string[]>;
const url = "/api/v1/applications";

const getApplications = async () => {
  const results = await apiGetApplications({
    queryKey: [url],
    meta: undefined,
  });
  return results;
};
</script>

<template>
  <p class="mb-0 fw-bold">Applications:</p>
  <FormKit
    type="multiselect"
    name="applications"
    placeholder="Choose applications"
    mode="tags"
    :msOptions="getApplications"
    searchable
    :close-on-select="false"
  />
</template>
