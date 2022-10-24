<script setup lang="ts">
import { apiGet } from "@/api";
import type { User } from "@/api/types";
import type { QueryFunction } from "react-query/types/core";
import { ref } from "vue";
import ArtifactsOwnedSummary from "./ArtifactsOwnedSummary.vue";

const props = defineProps<{
  initialvalue: string[];
  label: string;
  showArtifactsOwnedSummary?: boolean;
  placeholder?: string;
}>();

const value = ref<string[]>(props.initialvalue);

const apiGetUsers = apiGet as QueryFunction<{ users: User[] }>;
const url = "/api/v1/users";
const getUsers = async (query: string) => {
  const results = await apiGetUsers({
    queryKey: [url, { search: query }],
    meta: undefined,
  });
  return results;
};
</script>

<template>
  <FormKit
    type="multiselect"
    name="params"
    :label="props.label"
    label-class="fw-bold"
    mode="tags"
    :placeholder="props.placeholder"
    v-model="value"
    :msOptions="getUsers"
    :close-on-select="false"
    searchable
    :filter-results="false"
    :resolve-on-load="false"
    validation="required"
    :min-chars="3"
    :delay="0"
  />

  <ArtifactsOwnedSummary
    v-if="props.showArtifactsOwnedSummary"
    :users="value"
  />
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
