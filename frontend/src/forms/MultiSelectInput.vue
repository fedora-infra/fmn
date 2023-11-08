<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import type { FormKitFrameworkContext } from "@formkit/core";
import Multiselect from "@vueform/multiselect";
import type { VNode } from "vue";
import { computed } from "vue";
import { getBindableProps } from "./MultiSelectInputUtils";

const props = defineProps<{ context: FormKitFrameworkContext }>();

const bindableProps = computed(() => getBindableProps(props.context));
const slots = computed(
  () => props.context.slots as Partial<Multiselect["$slots"]>,
);

function handleChange(value: string) {
  props.context.node.input(value);
}

// This helped: https://codesandbox.io/s/0w1c1h?file=/src/FormKitMultiselect.vue
</script>

<template>
  <Multiselect v-bind="bindableProps" @change="handleChange">
    <template
      v-for="(slot, slotName) of slots"
      :key="slotName"
      v-slot:[slotName]="slotParams: VNode"
    >
      <component :is="slot" v-bind="slotParams" />
    </template>
  </Multiselect>
</template>

<style>
:root {
  --ms-font-size: var(--bs-body-font-size);
  --ms-line-height: var(--bs-body-line-height);
  --ms-option-font-size: var(--bs-body-font-size);
  --ms-option-line-height: var(--bs-body-line-height);
  /* For ms-py we actually want $input-btn-padding-y but it seems only available in SASS */
  --ms-py: var(--bs-border-radius);
  /* Box shadow color: in Bootstrap, it uses a SASS rule: tint-color(var(--bs-primary), 50%); */
  --ms-ring-color: rgba(60, 151, 214, 0.25);
}
.multiselect.is-open {
  --ms-border-color: #9ecbeb;
}
</style>
