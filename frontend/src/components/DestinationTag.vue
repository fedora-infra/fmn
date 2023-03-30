<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import type { Destination } from "@/api/types";
import { cilChatBubble, cilEnvelopeClosed } from "@coreui/icons";
import { CIcon } from "@coreui/icons-vue";
const props = defineProps<{
  destination: Destination;
  icononly: boolean;
}>();
const icon =
  props.destination.protocol === "email" ? cilEnvelopeClosed : cilChatBubble;
</script>

<template>
  <span
    class="me-2 d-inline-flex align-items-center"
    :class="{ 'badge border bg-light text-secondary': props.icononly }"
    v-c-tooltip="{
      content: `${props.destination.protocol}:${props.destination.address}`,
    }"
  >
    <CIcon :icon="icon" />
    <template v-if="!props.icononly"
      ><div class="pt-1 ps-1">
        <strong>{{ props.destination.protocol }}:</strong
        >{{ props.destination.address }}
      </div></template
    >
  </span>
</template>
