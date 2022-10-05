<script setup lang="ts">
import { apiGet } from "@/api";
import type { Artifact } from "@/api/types";
import type { QueryFunction } from "react-query/types/core";
import { useQuery } from "vue-query";
import TrackingRuleSummary from "./TrackingRuleSummary.vue";

const props = defineProps<{
  users?: string[];
  groups?: string[];
}>();

const route = "/artifacts/owned";
const { isLoading, isError, data, error } = useQuery(
  [route, { user: props.users, groups: props.groups }],
  apiGet as QueryFunction<Artifact[]>
);
</script>

<template>
  <span v-if="isLoading">Checking how many artifacts will be tracked…</span>
  <span v-else-if="isError"
    >Could not check how many artifacts will be tracked: {{ error }}</span
  >
  <TrackingRuleSummary v-else :tracked="data ? data.map((a) => a.name) : []" />
</template>
