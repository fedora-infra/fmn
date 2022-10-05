<script setup lang="ts">
import type { Destination } from "@/api/types";
import DestinationTag from "../../DestinationTag.vue";
const props = defineProps<{
  value: string;
}>();
const [protocol, address] = props.value.split(":", 2);
const d: Destination = { protocol, address };
</script>

<template>
  <DestinationTag :destination="d" />
</template>
