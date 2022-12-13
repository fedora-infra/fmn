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
const node = ref<{ node: FormKitNode } | null>(null);

const onTrackingRuleChange = (value: string, node: FormKitNode) => {
  // console.log("old tr name was", oldRuleName.value, ", new tr name is", value);
  if (value === oldRuleName.value) {
    return;
  }
  if (oldRuleName.value === "") {
    // oldRuleName is empty string on init, don't overwrite the params.
    oldRuleName.value = value;
    return;
  }
  oldRuleName.value = value;
  emit("selected", value);
  const paramsNode = node.at("params");
  const initialValue = value === "artifacts-owned" ? [username] : [];
  paramsNode?.input(initialValue);
};
</script>

<template>
  <FormKit type="group" name="tracking_rule">
    <FormKit
      type="multiselect"
      name="name"
      label="Tracking Rule:"
      label-class="fw-bold"
      placeholder="Choose a Tracking Rule"
      ref="node"
      v-model="ruleName"
      :msOptions="
        TRACKING_RULES.map((tr) => ({
          value: tr.name,
          label: tr.label,
          description: tr.description,
        }))
      "
      validation="required"
      @input="onTrackingRuleChange"
    >
      <template v-slot:option="{ option }">
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
