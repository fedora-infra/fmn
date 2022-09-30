<script setup lang="ts">
import type { GenerationRule } from "@/api/types";
import {
  CButton,
  CModal,
  CModalBody,
  CModalHeader,
  CModalTitle,
} from "@coreui/bootstrap-vue";
import type { FormKitNode } from "@formkit/core";
import { ref } from "vue";
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
    <!-- We can't use the default close button because it's not set with type="button" and formkit will think it's a submit button -->
    <CModalHeader :close-button="false">
      <CModalTitle>{{ props.title }}</CModalTitle>
      <CButton
        type="button"
        class="btn btn-close"
        aria-label="Close"
        @click="handleClose"
      />
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
      <NotificationPreview />
    </CModalBody>
  </CModal>
</template>
