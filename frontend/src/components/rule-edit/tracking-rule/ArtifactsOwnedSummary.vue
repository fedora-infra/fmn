<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { apiGet } from "@/api";
import type { APIError, Artifact } from "@/api/types";
import { CSpinner } from "@coreui/bootstrap-vue";
import { computed } from "vue";
import { useQuery } from "vue-query";
import TrackingRuleSummary from "./TrackingRuleSummary.vue";

const props = defineProps<{
  users?: string[];
  groups?: string[];
}>();

const route = "/api/v1/artifacts";
const queryParams = computed(() => ({
  users: props.users,
  groups: props.groups,
}));
const visible = computed(
  () =>
    (props.groups && props.groups.length > 0) ||
    (props.users && props.users.length > 0)
);
const { isLoading, isError, data, error } = useQuery<Artifact[], APIError>(
  [route, queryParams],
  apiGet,
  { enabled: visible.value }
);
</script>

<template>
  <div class="mt-3" v-if="visible">
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
