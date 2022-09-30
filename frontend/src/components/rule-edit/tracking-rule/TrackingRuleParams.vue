<script setup lang="ts">
import ArtifactsFollowedParams from "./ArtifactsFollowedParams.vue";
import ArtifactsGroupsOwnedParams from "./ArtifactsGroupsOwnedParams.vue";
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
      <ArtifactsGroupsOwnedParams />
    </template>
    <template v-if="props.ruleName == 'artifacts-followed'">
      <ArtifactsFollowedParams />
    </template>
    <template v-if="props.ruleName == 'users-followed'">
      <UsersFollowedParams />
    </template>
  </div>
</template>
