<script setup lang="ts">
import { apiGet } from "@/api";
import { ARTIFACT_TYPES } from "@/api/constants";
import type { Artifact } from "@/api/types";
import type { QueryFunction } from "react-query/types/core";
import { ref } from "vue";

const artifactName = ref<Record<string, string>[]>([]);
const artifactType = ref<Record<string, string> | string>("");
const apiGetArtifacts = apiGet as QueryFunction<{ artifacts: Artifact[] }>;
const route = "/artifacts/";
const getArtifacts = async (query: string) => {
  const results = await apiGetArtifacts({
    queryKey: [route, { type: artifactType.value, name: query }],
    meta: undefined,
  });
  return results
    ? results.artifacts.map((a) => ({ lablel: a.name, value: a.name }))
    : [];
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
        :msOptions="ARTIFACT_TYPES.map((t) => t.label)"
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
      :object="true"
      :disabled="artifactType === ''"
    />
  </FormKit>
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
