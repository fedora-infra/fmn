<!-- eslint-disable prettier/prettier -->
<script setup lang="ts">
import { SEVERITIES } from "../api/constants";
</script>

<template>
  <p class="mb-0">Only notify for the selected severities:</p>
  <FormKit
    type="multiselect"
    name="severities"
    placeholder="Select severities"
    mode="tags"
    :msOptions="SEVERITIES.map((s) => s.label)"
    :close-on-select="false"
  />
</template>
