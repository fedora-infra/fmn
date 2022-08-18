<script setup lang="ts">
import type { FormKitFrameworkContext } from "@formkit/core";
import Multiselect from "@vueform/multiselect";

const props = defineProps<{ context: FormKitFrameworkContext }>();
function handleChange(value: string) {
  props.context.node.input(value);
}

// This helped: https://codesandbox.io/s/0w1c1h?file=/src/FormKitMultiselect.vue
</script>

<template>
  <Multiselect
    :id="props.context.id"
    :name="props.context.node.name"
    :value="props.context._value"
    @change="handleChange"
    :disabled="props.context.disabled"
    v-bind="props.context.node.props"
    :options="props.context.node.props.msOptions"
  >
    <template
      v-for="(slot, slotName) of (props.context.slots as Record<string, () => void>)"
      :key="slotName"
      v-slot:[slotName]="slotParams"
    >
      <component :is="slot.bind(null, slotParams)" />
    </template>
  </Multiselect>
</template>
