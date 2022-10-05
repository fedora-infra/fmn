<script setup lang="ts">
import type { Destination } from "@/api/types";
import { cilChatBubble, cilEnvelopeClosed } from "@coreui/icons";
import { CIcon } from "@coreui/icons-vue";
const props = defineProps<{
  destination: Destination;
}>();
const icon =
  props.destination.protocol === "email" ? cilEnvelopeClosed : cilChatBubble;
</script>

<template>
  <span class="me-2 p-1 border border-info rounded bg-info bg-opacity-10">
    <CIcon :icon="icon" />
    {{ props.destination.address }}
  </span>
</template>
