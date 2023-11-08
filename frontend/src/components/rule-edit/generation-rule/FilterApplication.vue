<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { apiGet } from "@/api";

// const props = defineProps<{ value: string | null }>();

const url = "/api/v1/applications";

const getApplications = async () => {
  const results = await apiGet<string[]>({
    queryKey: [url],
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
