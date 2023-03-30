<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
//const props = defineProps<{ value: string | null }>();
//const emit = defineEmits(["change"]);
</script>

<template>
  <p class="mb-0 fw-bold">Topic pattern:</p>
  <FormKit
    type="text"
    name="topic"
    placeholder="Filter by topic pattern"
    help="Wildcards: * and ?"
  />
</template>
