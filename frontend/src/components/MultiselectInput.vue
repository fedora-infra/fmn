<script setup lang="ts">
import { FormKitFrameworkContext } from "@formkit/core";
import Multiselect from "@vueform/multiselect";

const props = defineProps<{ context: FormKitFrameworkContext }>();
function handleChange(value: string) {
  props.context.node.input(value);
}
</script>

<template>
  <Multiselect
    :id="props.context.id"
    :name="props.context.node.name"
    :value="props.context._value"
    @change="handleChange"
    :disabled="props.context.disabled"
    v-bind="context.node.props"
    :options="context.node.props.msOptions"
  >
    <slot />
  </Multiselect>
</template>
