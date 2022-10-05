<script setup lang="ts">
import type { GenerationRule } from "@/api/types";
import { CButton, CCard, CCardBody } from "@coreui/bootstrap-vue";
import { cilPlus } from "@coreui/icons";
import { CIcon } from "@coreui/icons-vue";
import { computed, ref } from "vue";
import GenerationRuleListItem from "./GenerationRuleListItem.vue";
import GenerationRuleModal from "./GenerationRuleModal.vue";

const props = defineProps<{
  rules?: GenerationRule[];
}>();

const emit = defineEmits<{
  (e: "change", rules: GenerationRule[]): void;
}>();

const generation_rules = ref<GenerationRule[]>([...(props.rules || [])]);
const editing = ref<number | null>(null);
const handleButtonClicked = (index: number) => {
  editing.value = index;
};
const handleRuleSubmitted = (rule: GenerationRule) => {
  if (editing.value === null) {
    return;
  } else if (editing.value === -1) {
    // New rule
    generation_rules.value.push(rule);
  } else {
    // Existing rule
    generation_rules.value[editing.value] = rule;
  }
  // Close the dialog
  editing.value = null;
  emit("change", generation_rules.value);
};
const handleRuleDeleted = (index: number) => {
  generation_rules.value.splice(index, 1);
  emit("change", generation_rules.value);
};
const handleModalClosed = () => {
  editing.value = null;
};
const modalVisible = computed(() => editing.value !== null);
const modalTitle = computed(() =>
  editing.value === -1 ? "Add Destination" : "Edit Destination"
);
const modalButtonLabel = computed(() =>
  editing.value === -1 ? "Add Destination" : "Save Destination"
);
const editedRule = computed(() =>
  editing.value !== null ? generation_rules.value[editing.value] : undefined
);
</script>

<template>
  <CCard class="border bg-light p-2">
    <CCardBody>
      <div v-if="generation_rules.length === 0">
        <h4 class="text-center text-muted my-4">No Destinations Defined</h4>
      </div>
      <FormKit
        v-else
        type="list"
        name="generation_rules"
        v-model="generation_rules"
      >
        <template v-for="(gr, index) in generation_rules" :key="gr.id">
          <GenerationRuleListItem
            :rule="gr"
            @edit="() => handleButtonClicked(index)"
            @delete="() => handleRuleDeleted(index)"
          />
        </template>
      </FormKit>
      <div class="text-center mt-4">
        <CButton
          @click="() => handleButtonClicked(-1)"
          :color="generation_rules.length === 0 ? 'primary' : 'secondary'"
          type="button"
        >
          <CIcon :icon="cilPlus" />
          Add Destination
        </CButton>
      </div>
    </CCardBody>
  </CCard>
  <GenerationRuleModal
    @submit="handleRuleSubmitted"
    @close="handleModalClosed"
    :visible="modalVisible"
    :title="modalTitle"
    :rule="editedRule"
    :button-label="modalButtonLabel"
  />
</template>
