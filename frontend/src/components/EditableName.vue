<script setup lang="ts">
import { CButton } from "@coreui/bootstrap-vue";
import { cilPen } from "@coreui/icons";
import { CIcon } from "@coreui/icons-vue";
import type { FormKitNode } from "@formkit/core";
import { FormKit } from "@formkit/vue";
import { onUpdated, ref } from "vue";

const props = defineProps<{
  name: string;
  value: string;
  buttonClass?: string;
  inputClass?: string;
}>();

const editing = ref(false);
const input = ref<{ node: FormKitNode } | null>(null);
const value = ref(props.value);
const toggleEditing = () => {
  editing.value = !editing.value;
};
onUpdated(() => {
  // Can't be done in toggleEditing because the dom node is still not displayed at that time.
  if (!editing.value || !input.value || !input.value.node.props.id) {
    return;
  }
  const domElement = document.getElementById(input.value.node.props.id);
  domElement?.focus();
});
</script>

<template>
  <span :class="{ 'd-none': !editing }">
    <FormKit
      type="text"
      :name="props.name"
      v-model="value"
      @blur="toggleEditing"
      @keyup.enter="toggleEditing"
      @keydown.enter.prevent
      ref="input"
      :input-class="props.inputClass"
    />
  </span>
  <span :class="{ 'd-none': editing }">
    {{ value }}
    <CButton
      color="link"
      @click.prevent="toggleEditing"
      :class="props.buttonClass"
    >
      <CIcon :icon="cilPen" class="align-baseline" />
    </CButton>
  </span>
</template>
