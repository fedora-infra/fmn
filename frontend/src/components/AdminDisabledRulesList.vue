<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import type { Rule } from "@/api/types";
import { CAccordion, CCard, CCardBody } from "@coreui/bootstrap-vue";
import AdminRuleListItem from "./AdminRuleListItem.vue";
import AdminRuleDisableForm from "./AdminRuleDisableForm.vue";

const props = defineProps<{
  rules: Rule[];
}>();
</script>

<template>
  <div
    class="d-flex justify-content-between align-items-center w-100 bg-light border rounded-top py-3 px-3"
  >
    <h4 class="mb-0">{{ props.rules.length }} Disabled Rules</h4>
    <AdminRuleDisableForm />
  </div>
  <CCard v-if="rules.length === 0" class="border bg-light py-5">
    <CCardBody>
      <h2 class="text-center text-muted">No Disabled Rules.</h2>
    </CCardBody>
  </CCard>
  <template v-else>
    <CAccordion>
      <AdminRuleListItem
        v-for="rule in props.rules"
        :key="rule.id"
        :rule="rule"
      />
    </CAccordion>
  </template>
</template>
