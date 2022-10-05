<script setup lang="ts">
import type { GenerationRule } from "@/api/types";
import { CButton } from "@coreui/bootstrap-vue";
import { cilPen, cilTrash } from "@coreui/icons";
import { CIcon } from "@coreui/icons-vue";
import DestinationTag from "../../DestinationTag.vue";

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
  <div class="d-flex align-items-center">
    <span class="me-auto">
      <DestinationTag
        :destination="dest"
        v-for="dest in props.rule.destinations"
        :key="`${dest.protocol}:${dest.address}`"
      />
    </span>
    <span>
      <span>X avg messages a day</span>
      <CButton
        @click="handleEditClicked"
        color="primary"
        type="button"
        variant="outline"
        class="ms-1"
      >
        <CIcon :icon="cilPen" />
      </CButton>
      <CButton
        @click="handleDeleteClicked"
        color="danger"
        type="button"
        variant="outline"
        class="ms-1"
      >
        <CIcon :icon="cilTrash" />
      </CButton>
    </span>
  </div>
</template>
