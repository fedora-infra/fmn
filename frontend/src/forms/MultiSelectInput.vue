<script setup lang="ts">
import type { FormKitFrameworkContext, FormKitProps } from "@formkit/core";
import Multiselect from "@vueform/multiselect";
import { computed } from "vue";
import { msProps } from "./MultiSelectInputConstants";

const props = defineProps<{ context: FormKitFrameworkContext }>();

const bindableProps = computed(() => {
  const val: Partial<FormKitProps> = Object.keys(props.context.node.props)
    .filter((key) => msProps.includes(key))
    .reduce(
      (obj, key) =>
        Object.assign(obj, { [key]: props.context.node.props[key] }),
      {}
    );
  val.id = props.context.id;
  val.name = props.context.name;
  val.value = props.context._value;
  val.disabled = props.context.disabled;
  val.options = props.context.node.props.msOptions;
  val.label = props.context.node.props.msLabel;
  return val;
});

function handleChange(value: string) {
  props.context.node.input(value);
}

// This helped: https://codesandbox.io/s/0w1c1h?file=/src/FormKitMultiselect.vue
</script>

<template>
  <Multiselect v-bind="bindableProps" @change="handleChange">
    <template
      v-for="(slot, slotName) of (props.context.slots as Record<string, () => void>)"
      :key="slotName"
      v-slot:[slotName]="slotParams"
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
