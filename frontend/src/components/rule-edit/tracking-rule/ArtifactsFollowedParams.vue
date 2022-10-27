<script setup lang="ts">
import { apiGet } from "@/api";
import { ARTIFACT_TYPES } from "@/api/constants";
import type { Artifact } from "@/api/types";
import type { QueryFunction } from "react-query/types/core";
import { ref } from "vue";

const artifactName = ref<string[]>([]);
const artifactType = ref<string>("");
const apiGetArtifacts = apiGet as QueryFunction<{ artifacts: Artifact[] }>;
const route = "/api/v1/artifacts";
const getArtifacts = async (query: string) => {
  const results = await apiGetArtifacts({
    queryKey: [route, { type: artifactType.value, name: query }],
    meta: undefined,
  });
  return results ? results.artifacts.map((a) => a.name) : [];
};
</script>

<template>
  <FormKit type="group" name="params">
    <div class="mb-2">
      <FormKit
        type="multiselect"
        name="type"
        label="Artifact type:"
        label-class="fw-bold"
        placeholder="Choose an Artifact Type"
        :msOptions="ARTIFACT_TYPES"
        v-model="artifactType"
      />
    </div>
    <FormKit
      type="multiselect"
      name="name"
      label="Artifact names:"
      label-class="fw-bold"
      mode="tags"
      v-model="artifactName"
      :msOptions="getArtifacts"
      :close-on-select="false"
      searchable
      :filter-results="false"
      :resolve-on-load="false"
      validation="required"
      :delay="0"
      :min-chars="1"
      :disabled="artifactType === ''"
      placeholder="Search by artifact name"
      noOptionsText="No matches on that artifact found"
    />
  </FormKit>
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
