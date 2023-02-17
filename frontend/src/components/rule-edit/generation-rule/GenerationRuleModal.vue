<script setup lang="ts">
import type { GenerationRule, NewRule } from "@/api/types";
import {
  CModal,
  CModalBody,
  CModalHeader,
  CModalTitle,
} from "@coreui/bootstrap-vue";
import type { FormKitNode } from "@formkit/core";
import { computed, ref } from "vue";
import DestinationList from "./DestinationList.vue";
import FilterList from "./FilterList.vue";
import NotificationPreview from "./NotificationPreview.vue";

const props = defineProps<{
  visible: boolean;
  rule?: GenerationRule;
  title: string;
  buttonLabel: string;
}>();
const emit = defineEmits<{
  (e: "submit", rule: GenerationRule): void;
  (e: "close"): void;
}>();

const node = ref<{ node: FormKitNode } | null>(null);
const previzData = computed(() => {
  if (!node.value) {
    return null;
  }
  const root = node.value.node.at("$root");
  if (!root || !root.context) {
    return null;
  }
  const result: NewRule = {
    name: root.context._value.name as string,
    disabled: false,
    tracking_rule: root.context._value
      .tracking_rule as NewRule["tracking_rule"],
    generation_rules: [node.value.node.value as GenerationRule],
  };
  return result;
});

const handleSubmit = async (data: GenerationRule) => {
  emit("submit", data);
};
const handleClose = async () => {
  emit("close");
};
</script>

<template>
  <CModal
    :visible="props.visible"
    size="lg"
    scrollable
    backdrop="static"
    @close="handleClose"
  >
    <!-- Catch and prevent the click event on the close button so that it does not submit the form -->
    <CModalHeader @click.prevent="">
      <CModalTitle>{{ props.title }}</CModalTitle>
    </CModalHeader>
    <CModalBody>
      <FormKit
        type="form"
        ref="node"
        @submit="handleSubmit"
        :actions="false"
        :value="props.rule"
      >
        <DestinationList />
        <FilterList />
        <div class="text-center my-4">
          <FormKit type="submit" :class="['btn', 'btn-primary']">{{
            props.buttonLabel
          }}</FormKit>
        </div>
      </FormKit>
      <NotificationPreview v-if="previzData" :data="previzData" />
    </CModalBody>
  </CModal>
</template>
