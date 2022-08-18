<!-- eslint-disable prettier/prettier -->
<script setup lang="ts">
import { SEVERITIES } from "../api/constants";
import FilterWithSelect from "./FilterWithSelect.vue";

//const props = defineProps<{ value: string | null }>();
</script>

<template>
  <p class="mb-0">Only notify for the selected severity:</p>
  <FilterWithSelect name="severity" :options="SEVERITIES.map((s) => s.label)" />
</template>
