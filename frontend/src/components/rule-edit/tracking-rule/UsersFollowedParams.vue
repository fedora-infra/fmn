<script setup lang="ts">
import UserMultiSelect from "./UserMultiSelect.vue";
</script>

<template>
  <UserMultiSelect
    :initialvalue="[]"
    label="Users:"
    placeholder="Search for users by username"
  />
</template>
