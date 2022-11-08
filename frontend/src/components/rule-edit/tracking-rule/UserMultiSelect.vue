<script setup lang="ts">
import { apiGet } from "@/api";
import type { User } from "@/api/types";
import { useUserStore } from "@/stores/user";
import type { QueryFunction } from "react-query/types/core";
import { ref } from "vue";
import ArtifactsOwnedSummary from "./ArtifactsOwnedSummary.vue";

const props = defineProps<{
  label: string;
  showArtifactsOwnedSummary?: boolean;
  placeholder?: string;
  nooptionstext?: string;
}>();

const userStore = useUserStore();
const value = ref<string[]>([]);

const apiGetUsers = apiGet as QueryFunction<User[]>;
const url = "/api/v1/users";

const getUsers = async (query: string) => {
  if (!query) {
    // This is required because of resolve-on-load, which is needed because we have a default value.
    return userStore.username ? [userStore.username] : [];
  }
  const results = await apiGetUsers({
    queryKey: [url, { search: query }],
    meta: undefined,
  });
  return results;
};
const getUsersAsOptions = async (query: string) => {
  // According to Multiselect's API, we must return a list of objects when using an async function for options.
  const result = await getUsers(query);
  return result.map((value) => ({
    label: value,
    value: value,
  }));
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
    :noOptionsText="props.nooptionstext"
    v-model="value"
    :msOptions="getUsersAsOptions"
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
