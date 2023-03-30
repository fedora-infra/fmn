<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
//const props = defineProps<{ value: boolean }>();
//const emit = defineEmits(["change"]);
</script>

<template>
  <p class="mb-0 fw-bold">My Actions:</p>
  <FormKit
    type="checkbox"
    name="my_actions"
    label="Including actions I initiated"
  />
</template>
