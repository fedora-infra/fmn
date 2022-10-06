<script setup lang="ts">
import { apiGet } from "@/api";
import type { Artifact } from "@/api/types";
import { CSpinner } from "@coreui/bootstrap-vue";
import type { QueryFunction } from "react-query/types/core";
import { useQuery } from "vue-query";
import TrackingRuleSummary from "./TrackingRuleSummary.vue";

const props = defineProps<{
  users?: string[];
  groups?: string[];
}>();

const route = "/artifacts/owned";
const { isLoading, isError, data, error } = useQuery(
  [route, { users: props.users, groups: props.groups }],
  apiGet as QueryFunction<Artifact[]>
);
</script>

<template>
  <div class="mt-3">
    <p v-if="isLoading">
      Checking how many artifacts will be tracked…
      <CSpinner size="sm" />
    </p>
    <p v-else-if="isError">
      Could not check how many artifacts will be tracked: {{ error }}
    </p>
    <TrackingRuleSummary v-else-if="data" :tracked="data" />
  </div>
</template>
