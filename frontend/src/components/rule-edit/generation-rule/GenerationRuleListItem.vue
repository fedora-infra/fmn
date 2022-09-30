<script setup lang="ts">
import type { GenerationRule } from "@/api/types";
import { CButton } from "@coreui/bootstrap-vue";
import { cilPen, cilTrash } from "@coreui/icons";
import { CIcon } from "@coreui/icons-vue";

const props = defineProps<{
  rule: GenerationRule;
}>();

const emit = defineEmits<{
  (e: "edit"): void;
  (e: "delete"): void;
}>();

const handleEditClicked = () => {
  emit("edit");
};
const handleDeleteClicked = () => {
  emit("delete");
};
</script>

<template>
  <div class="border">
    <span>{{ props.rule.destinations }} - {{ props.rule.filters }}</span>
    <CButton
      @click="handleEditClicked"
      color="primary"
      type="button"
      variant="outline"
    >
      <CIcon :icon="cilPen" />
    </CButton>
    <CButton
      @click="handleDeleteClicked"
      color="danger"
      type="button"
      variant="outline"
    >
      <CIcon :icon="cilTrash" />
    </CButton>
  </div>
</template>
