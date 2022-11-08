<script setup lang="ts">
import { apiGet } from "@/api";
import type { Group } from "@/api/types";
import { useUserStore } from "@/stores/user";
import type { QueryFunction } from "react-query/types/core";
import { onUnmounted, ref } from "vue";
import { useQuery, useQueryClient } from "vue-query";
import ArtifactsOwnedSummary from "./ArtifactsOwnedSummary.vue";

const userStore = useUserStore();
const value = ref<string[]>([]);
const apiGetUserGroups = apiGet as QueryFunction<Group[]>;
const url = `/api/v1/users/${userStore.username}/groups`;
const { isLoading, isError, data, error } = useQuery(url, apiGetUserGroups);
onUnmounted(async () => {
  const client = useQueryClient();
  await client.cancelQueries([url]);
});
</script>

<template>
  <p v-if="isLoading">
    <input
      type="text"
      class="form-control"
      disabled
      value="Loading groups..."
    />
  </p>
  <span v-else-if="isError">Could not load groups: {{ error }}</span>
  <template v-else>
    <FormKit
      type="multiselect"
      name="params"
      label="Artifacts owned by groups:"
      label-class="fw-bold"
      mode="tags"
      v-model="value"
      :msOptions="data || []"
      searchable
      :close-on-select="false"
      validation="required"
    />
    <ArtifactsOwnedSummary :groups="value" />
  </template>
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
