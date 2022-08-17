<script setup lang="ts">
import { TRACKING_RULES } from "../api/constants";
</script>

<template>
  <FormKit
    type="multiselect"
    name="tracking_rule"
    wrapper-class="$reset"
    inner-class="$reset"
    placeholder="Choose a Tracking Rule"
    :msOptions="
      TRACKING_RULES.map((tr) => ({
        value: tr.name,
        label: tr.label,
        description: tr.description,
      }))
    "
    searchable
    validation="required"
  >
    <template v-slot:option="{ option }">
      <div>
        <strong>{{ option.label }}</strong>
        <div>{{ option.description }}</div>
      </div>
    </template>
  </FormKit>
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
