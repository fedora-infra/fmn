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

/*
 * This is useful when we want to have a default value and an async loader.
 * https://github.com/vueform/multiselect#async-options-with-default-values
 */

const props = defineProps<{ context: FormKitFrameworkContext }>();
const slots = computed(
  () => props.context.slots as Partial<Multiselect["$slots"]>,
);

type Option = { [key in "label" | "value"]: string };

const simpleValueToOption = (value: string): Option => ({
  label: value,
  value: value,
});
const valueToOption =
  props.context.node.props.msValueToOption || simpleValueToOption;

const simpleResultsToOptions = (values: string[]): Option[] =>
  values.map(valueToOption);

const resultsToOptions =
  props.context.node.props.msResultsToOptions || simpleResultsToOptions;

const getAsOptions = async (query: string, select$: Multiselect) => {
  // According to Multiselect's API, we must return a list of objects when using an async function for options.
  const result = await props.context.node.props.msOptions(query, select$);
  return resultsToOptions(result || []);
};

const bindableProps = computed(() => {
  const values = getBindableProps(props.context);
  values.object = true;
  values.options = getAsOptions;
  values.value = (props.context._value || []).map(valueToOption);
  return values;
});

function handleChange(value: Option[]) {
  props.context.node.input(value.map((v) => v.value));
}

// This helped: https://codesandbox.io/s/0w1c1h?file=/src/FormKitMultiselect.vue
</script>

<template>
  <Multiselect v-bind="bindableProps" @change="handleChange">
    <template
      v-for="(slot, slotName) in slots"
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
