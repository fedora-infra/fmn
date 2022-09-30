<script setup lang="ts">
import { apiGet } from "@/api";
import type { User } from "@/api/types";
import { useUserStore } from "@/stores/user";
import type { QueryFunction } from "react-query/types/core";
import { ref } from "vue";
import ArtifactsOwnedSummary from "./ArtifactsOwnedSummary.vue";

const userStore = useUserStore();
const username = userStore.username!;
const value = ref<Record<string, string>[]>([
  { label: username, value: username },
]);
const apiGetUsers = apiGet as QueryFunction<{ users: User[] }>;
const route = "/users/";
const getUsers = async (query: string) => {
  const results = await apiGetUsers({
    queryKey: [route, { search: query }],
    meta: undefined,
  });
  return results
    ? results.users.map((u) => ({ lablel: u.name, value: u.name }))
    : [];
};
</script>

<template>
  <FormKit
    type="multiselect"
    name="params"
    label="Artifacts owned by:"
    label-class="fw-bold"
    mode="tags"
    v-model="value"
    :msOptions="getUsers"
    :close-on-select="false"
    searchable
    :filter-results="false"
    :resolve-on-load="false"
    validation="required"
    :min-chars="3"
    :delay="0"
    :object="true"
  />
  <ArtifactsOwnedSummary :users="value.map((v) => v.value)" />
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
