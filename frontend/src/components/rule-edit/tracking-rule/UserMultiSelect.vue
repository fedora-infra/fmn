<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { apiGet } from "@/api";
import type { User } from "@/api/types";
import type { FormKitNode } from "@formkit/core";
import { ref } from "vue";
import ArtifactsOwnedSummary from "./ArtifactsOwnedSummary.vue";

const props = defineProps<{
  label: string;
  showArtifactsOwnedSummary?: boolean;
  placeholder?: string;
  nooptionstext?: string;
  initialValue?: string[];
}>();

const value = ref<string[]>([]);

const onNode = (node: FormKitNode) => {
  if (props.initialValue) {
    node.input(props.initialValue);
  }
};

const url = "/api/v1/users";

const getUsers = async (query: string) => {
  if (!query) {
    return [];
  }
  const results = await apiGet<User[]>({
    queryKey: [url, { search: query }],
  });
  return results;
};
</script>

<template>
  <FormKit
    type="multiselectasyncdefault"
    @node="onNode"
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
    :users="value"
  />
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
