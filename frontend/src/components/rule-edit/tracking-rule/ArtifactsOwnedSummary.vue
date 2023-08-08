<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { useArtifactsQuery } from "@/api/artifacts";
import { CSpinner } from "@coreui/bootstrap-vue";
import { computed, toRefs } from "vue";
import TrackingRuleSummary from "./TrackingRuleSummary.vue";

const props = defineProps<{
  users?: string[];
  groups?: string[];
}>();

const { groups, users } = toRefs(props);

const visible = computed(
  () =>
    (props.groups && props.groups.length > 0) ||
    (props.users && props.users.length > 0),
);
const { isLoading, isError, data, error } = useArtifactsQuery(users, groups);
</script>

<template>
  <div class="mt-3" v-if="visible">
    <p v-if="isLoading">
      Checking how many artifacts will be tracked…
      <CSpinner size="sm" />
    </p>
    <p v-else-if="isError">
      Could not check how many artifacts will be tracked: {{ error?.detail }}
    </p>
    <TrackingRuleSummary v-else-if="data" :tracked="data" />
  </div>
</template>
