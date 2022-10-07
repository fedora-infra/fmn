<script setup lang="ts">
import { TRACKING_RULES } from "@/api/constants";
import { ref } from "vue";
import TrackingRuleParams from "./TrackingRuleParams.vue";

const emit = defineEmits<{
  (e: "selected", name: string): void;
}>();

const ruleName = ref("");
</script>

<template>
  <FormKit type="group" name="tracking_rule">
    <FormKit
      type="multiselect"
      name="name"
      label="Tracking Rule:"
      label-class="fw-bold"
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
      @input="(value) => emit('selected', value)"
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
