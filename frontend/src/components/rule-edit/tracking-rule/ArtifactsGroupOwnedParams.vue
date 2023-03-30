<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { apiGet } from "@/api";
import { useUserStore } from "@/stores/user";
import type { QueryFunction } from "react-query/types/core";
import { ref } from "vue";
import ArtifactsOwnedSummary from "./ArtifactsOwnedSummary.vue";

const userStore = useUserStore();
const value = ref<string[]>([]);
const apiGetUserGroups = apiGet as QueryFunction<string[]>;
const url = `/api/v1/users/${userStore.username}/groups`;

const getUserGroups = async () => {
  const results = await apiGetUserGroups({
    queryKey: [url],
    meta: undefined,
  });
  return results;
};
</script>

<template>
  <FormKit
    type="multiselect"
    name="params"
    label="Artifacts owned by groups:"
    label-class="fw-bold"
    mode="tags"
    v-model="value"
    :msOptions="getUserGroups"
    :close-on-select="false"
    searchable
    :filter-results="false"
    :resolve-on-load="true"
  />
  <ArtifactsOwnedSummary :groups="value" />
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
