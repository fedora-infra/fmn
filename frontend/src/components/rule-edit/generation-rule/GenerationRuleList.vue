<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import type { GenerationRule } from "@/api/types";
import { CButton, CListGroup, CListGroupItem } from "@coreui/bootstrap-vue";
import { cilPlus } from "@coreui/icons";
import { CIcon } from "@coreui/icons-vue";
import type { FormKitNode } from "@formkit/core";
import { computed, ref, toRefs } from "vue";
import GenerationRuleListItem from "./GenerationRuleListItem.vue";
import GenerationRuleModal from "./GenerationRuleModal.vue";

const props = defineProps<{
  rules?: GenerationRule[];
}>();

const emit = defineEmits<{
  (e: "change", rules: GenerationRule[]): void;
}>();

const { rules } = toRefs(props);
const generationRulesInput = ref<{ node: FormKitNode } | null>(null);
const generation_rules = ref<GenerationRule[]>([...(rules?.value || [])]);
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
  // Update the main FormKit object
  generationRulesInput.value?.node.input(generation_rules.value);
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
  editing.value === -1 ? "Add Destination" : "Edit Destination",
);
const modalButtonLabel = computed(() =>
  editing.value === -1 ? "Add Destination" : "Save Destination",
);
const editedRule = computed(() =>
  editing.value !== null ? generation_rules.value[editing.value] : undefined,
);
</script>

<template>
  <CListGroup>
    <FormKit
      v-if="generation_rules.length > 0"
      type="list"
      name="generation_rules"
      v-model="generation_rules"
      ref="generationRulesInput"
    >
      <template v-for="(gr, index) in generation_rules" :key="gr.id">
        <GenerationRuleListItem
          :rule="gr"
          @edit="() => handleButtonClicked(index)"
          @delete="() => handleRuleDeleted(index)"
        />
      </template>
    </FormKit>
    <CListGroupItem class="bg-light">
      <h4
        v-if="generation_rules.length === 0"
        class="text-center text-muted my-4"
      >
        No Destinations Defined
      </h4>
      <div class="text-center">
        <CButton
          @click.prevent="() => handleButtonClicked(-1)"
          color="primary"
          :variant="generation_rules.length === 0 ? undefined : 'outline'"
          class="my-1"
        >
          <CIcon :icon="cilPlus" />
          <template v-if="generation_rules.length === 0"
            >Add Destination</template
          >
          <template v-else>Add Another Destination</template>
        </CButton>
      </div>
    </CListGroupItem>
  </CListGroup>
  <GenerationRuleModal
    @submit="handleRuleSubmitted"
    @close="handleModalClosed"
    :visible="modalVisible"
    :title="modalTitle"
    :rule="editedRule"
    :button-label="modalButtonLabel"
  />
</template>
