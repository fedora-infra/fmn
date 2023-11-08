<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { TRACKING_RULES } from "@/api/constants";
import { useUserStore } from "@/stores/user";
import type { FormKitNode } from "@formkit/core";
import { ref } from "vue";
import TrackingRuleParams from "./TrackingRuleParams.vue";
const emit = defineEmits<{
  (e: "selected", name: string): void;
}>();

const userStore = useUserStore();
const username = userStore.username;

const ruleName = ref("");
const oldRuleName = ref<string | null>("");

const setParamsValue = (trValue: string, trNode: FormKitNode) => {
  // console.log("tr name was", oldRuleName.value, ", changed to", trValue);
  if (trValue === oldRuleName.value) {
    return; // no change
  }
  oldRuleName.value = trValue;
  emit("selected", trValue);
  // Pre-fill the parameters with sensible defaults
  const paramsNode = trNode.at("params");
  if (!paramsNode) {
    return;
  }

  let initialValue: string[] = [];
  if (trValue === "artifacts-owned" && username) {
    initialValue = [username];
  }
  // console.log("Setting initial params value to", initialValue);
  paramsNode.input(initialValue);
};

const onNode = (node: FormKitNode) => {
  // Init the oldRuleName value to detect changes
  const value = (node.value || "") as string;
  oldRuleName.value = value;
  // This seems necessary for unit tests, not sure why v-model is not sufficient
  ruleName.value = value;
};
const onInput = (value: string, node: FormKitNode) => {
  return setParamsValue(value, node);
};
</script>

<template>
  <FormKit type="group" name="tracking_rule">
    <FormKit
      type="multiselect"
      name="name"
      label="Tracking Rule:"
      label-class="fw-bold mt-2"
      placeholder="Choose a Tracking Rule"
      v-model="ruleName"
      :msOptions="
        TRACKING_RULES.map((tr) => ({
          value: tr.name,
          label: tr.label,
          description: tr.description,
        }))
      "
      validation="required"
      @node="onNode"
      @input="onInput"
    >
      <template #option="{ option }">
        <div>
          <strong>{{ option.label }}</strong>
          <div>{{ option.description }}</div>
        </div>
      </template>
    </FormKit>

    <TrackingRuleParams v-if="ruleName" :ruleName="ruleName" />
  </FormKit>
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
<style>
:root {
  --ms-max-height: 20rem;
}
</style>
