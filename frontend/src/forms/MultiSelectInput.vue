<script setup lang="ts">
import type { FormKitFrameworkContext } from "@formkit/core";
import Multiselect from "@vueform/multiselect";

const props = defineProps<{ context: FormKitFrameworkContext }>();
/* eslint-disable */
// error  Getting a value from the `props` in root scope of `<script setup>` will cause the value to lose reactivity  vue/no-setup-props-destructure
const { msOptions, ...msProps } = props.context.node.props;
msProps.options = msOptions;
msProps.id = props.context.id;
msProps.name = props.context.node.name;
msProps.value = props.context._value;
msProps.disabled = props.context.disabled;
/* eslint-enable */

function handleChange(value: string) {
  props.context.node.input(value);
}

// This helped: https://codesandbox.io/s/0w1c1h?file=/src/FormKitMultiselect.vue
</script>

<template>
  <Multiselect v-bind="msProps" @change="handleChange">
    <template
      v-for="(slot, slotName) of (props.context.slots as Record<string, () => void>)"
      :key="slotName"
      v-slot:[slotName]="slotParams"
    >
      <component :is="slot.bind(null, slotParams)" />
    </template>
  </Multiselect>
</template>
