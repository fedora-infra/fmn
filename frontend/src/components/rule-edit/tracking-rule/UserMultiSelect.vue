<script setup lang="ts">
import { apiGet } from "@/api";
import type { User } from "@/api/types";
import type { QueryFunction } from "react-query/types/core";
import { ref } from "vue";
import ArtifactsOwnedSummary from "./ArtifactsOwnedSummary.vue";

const props = defineProps<{
  label: string;
  showArtifactsOwnedSummary?: boolean;
  placeholder?: string;
  nooptionstext?: string;
}>();

const value = ref<string[]>([]);

const apiGetUsers = apiGet as QueryFunction<User[]>;
const url = "/api/v1/users";

const getUsers = async (query: string) => {
  if (!query) {
    return [];
  }
  const results = await apiGetUsers({
    queryKey: [url, { search: query }],
    meta: undefined,
  });
  return results;
};
</script>

<template>
  <FormKit
    type="multiselectasyncdefault"
    name="params"
    :label="props.label"
    label-class="fw-bold"
    mode="tags"
    :placeholder="props.placeholder"
    :noOptionsText="props.nooptionstext"
    v-model="value"
    :msOptions="getUsers"
    :close-on-select="false"
    searchable
    :filter-results="false"
    :resolve-on-load="true"
    validation="required"
    :min-chars="3"
    :delay="0"
    :clearOnSearch="true"
  />

  <ArtifactsOwnedSummary
    v-if="props.showArtifactsOwnedSummary"
    :users="value || []"
  />
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
