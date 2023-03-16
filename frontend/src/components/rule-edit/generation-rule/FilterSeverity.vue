<!-- eslint-disable prettier/prettier -->
<script setup lang="ts">
import { SEVERITIES } from "@/api/constants";
</script>

<template>
  <p class="mb-0 fw-bold">Priorities:</p>
  <FormKit
    type="multiselect"
    name="severities"
    placeholder="Choose priorities"
    mode="tags"
    :msOptions="SEVERITIES.map((s) => s.label)"
    :close-on-select="false"
  />
</template>
