<script setup lang="ts">
import UserMultiSelect from "./UserMultiSelect.vue";
</script>

<template>
  <UserMultiSelect
    :initialvalue="[]"
    label="Users Pants:"
    placeholder="Search for users by username pants"
  />
</template>
