<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import ArtifactsFollowedParams from "./ArtifactsFollowedParams.vue";
import ArtifactsGroupOwnedParams from "./ArtifactsGroupOwnedParams.vue";
import ArtifactsOwnedParams from "./ArtifactsOwnedParams.vue";
import UsersFollowedParams from "./UsersFollowedParams.vue";
const props = defineProps<{
  ruleName: string;
}>();
</script>

<template>
  <div class="mt-3">
    <template v-if="props.ruleName == 'artifacts-owned'">
      <ArtifactsOwnedParams />
    </template>
    <template v-if="props.ruleName == 'artifacts-group-owned'">
      <ArtifactsGroupOwnedParams />
    </template>
    <template v-if="props.ruleName == 'artifacts-followed'">
      <ArtifactsFollowedParams />
    </template>
    <template v-if="props.ruleName == 'users-followed'">
      <UsersFollowedParams />
    </template>
  </div>
</template>
