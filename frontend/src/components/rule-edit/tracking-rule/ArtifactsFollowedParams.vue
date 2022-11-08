<script setup lang="ts">
import { apiGet } from "@/api";
import type { Artifact } from "@/api/types";
import type { QueryFunction } from "react-query/types/core";

const apiGetArtifacts = apiGet as QueryFunction<{ artifacts: Artifact[] }>;
const route = "/api/v1/artifacts";
const getArtifacts = async (query: string) => {
  const results = await apiGetArtifacts({
    queryKey: [route, { name: query }],
    meta: undefined,
  });
  return results;
};
</script>

<template>
  <FormKit
    type="multiselect"
    name="params"
    label="Artifact names:"
    label-class="fw-bold"
    mode="tags"
    :groups="true"
    :msOptions="getArtifacts"
    :close-on-select="false"
    searchable
    :filter-results="false"
    :resolve-on-load="false"
    validation="required"
    :delay="500"
    :min-chars="1"
    placeholder="Search by artifact name"
    noOptionsText="No matches on that artifact found"
  />
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
