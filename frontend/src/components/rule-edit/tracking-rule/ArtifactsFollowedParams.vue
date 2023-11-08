<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { apiGet } from "@/api";
import { ARTIFACT_CATEGORIES, ARTIFACT_CATEGORY_LABELS } from "@/api/constants";
import type { Artifact } from "@/api/types";

type Option = { label: string; value: Artifact };
type OptionGroup = { label: string; options: Option[] };

const valueToOption = (artifact: Artifact) => ({
  label: `${artifact.type}/${artifact.name}`,
  value: artifact,
});

const resultsToOptions = (results: Artifact[]) => {
  const options: OptionGroup[] = ARTIFACT_CATEGORIES.map((category) => ({
    label: category.label,
    options: [],
  }));
  results.forEach((artifact) => {
    const category = options.filter(
      (o) => o.label === ARTIFACT_CATEGORY_LABELS[artifact.type],
    )[0];
    category.options.push({
      label: `${artifact.type}/${artifact.name}`,
      value: artifact,
    });
  });
  return options;
};

const route = "/api/v1/artifacts";
const getArtifacts = async (query: string) => {
  const results = await apiGet<Artifact[]>({
    queryKey: [route, { names: `*${query}*` }],
  });
  return results;
};
</script>

<template>
  <FormKit
    type="multiselectasyncdefault"
    name="params"
    label="Artifact names:"
    label-class="fw-bold"
    mode="tags"
    :groups="true"
    :msOptions="getArtifacts"
    :close-on-select="false"
    searchable
    :filter-results="false"
    :resolve-on-load="false"
    validation="required"
    :delay="500"
    :min-chars="1"
    placeholder="Search by artifact name"
    noOptionsText="No matches on that artifact found"
    :msResultsToOptions="resultsToOptions"
    :msValueToOption="valueToOption"
  />
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
