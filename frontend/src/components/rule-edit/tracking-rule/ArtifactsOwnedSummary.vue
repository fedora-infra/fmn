<script setup lang="ts">
import { apiGet } from "@/api";
import type { Artifact } from "@/api/types";
import { CSpinner } from "@coreui/bootstrap-vue";
import type { QueryFunction } from "react-query/types/core";
import { computed } from "vue";
import { useQuery } from "vue-query";
import TrackingRuleSummary from "./TrackingRuleSummary.vue";

const props = defineProps<{
  users?: string[];
  groups?: string[];
}>();

const route = "/api/v1/artifacts/owned";
const queryParams = computed(() => ({
  users: props.users,
  groups: props.groups,
}));
const { isLoading, isError, data, error } = useQuery(
  [route, queryParams],
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
