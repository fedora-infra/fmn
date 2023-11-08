<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { apiGet } from "@/api";
import { useUserStore } from "@/stores/user";
import { ref } from "vue";
import ArtifactsOwnedSummary from "./ArtifactsOwnedSummary.vue";

const userStore = useUserStore();
const value = ref<string[]>([]);
const url = `/api/v1/users/${userStore.username}/groups`;

const getUserGroups = async () => {
  const results = await apiGet<string[]>({
    queryKey: [url],
  });
  return results;
};
</script>

<template>
  <FormKit
    type="multiselectasyncdefault"
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
    validation="required"
  />
  <ArtifactsOwnedSummary :groups="value" />
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
