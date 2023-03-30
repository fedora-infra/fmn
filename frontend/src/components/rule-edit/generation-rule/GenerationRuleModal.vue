<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import type { GenerationRule } from "@/api/types";
import {
  CModal,
  CModalBody,
  CModalHeader,
  CModalTitle,
} from "@coreui/bootstrap-vue";
import type { FormKitNode } from "@formkit/core";
import { ref } from "vue";
import DestinationList from "./DestinationList.vue";
import FilterList from "./FilterList.vue";

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
    size="lg"
    scrollable
    :visible="props.visible"
    @close="handleClose"
    alignment="center"
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
    </CModalBody>
  </CModal>
</template>
