<script setup lang="ts">
import {
  CAccordionBody,
  CAccordionHeader,
  CAccordionItem,
} from "@coreui/bootstrap-vue";

import AdminRuleEnableForm from "../components/AdminRuleEnableForm.vue";

import type { Rule } from "../api/types";
const props = defineProps<{
  rule: Rule;
}>();
</script>

<template>
  <CAccordionItem :item-key="props.rule.id" class="rounded-0">
    <CAccordionHeader>
      <div class="d-flex justify-content-between align-items-center w-100 pe-3">
        <div>
          <div>
            <strong>Rule ID: {{ props.rule.id }}</strong>
          </div>
          <div>
            <small
              ><strong>{{ props.rule.user.name }}'s</strong>
              {{ props.rule.name }}</small
            >
          </div>
        </div>
        <div>
          <span class="badge bg-primary me-1">{{
            rule.tracking_rule.name
          }}</span>
          <span class="badge bg-secondary"
            >Generation Rules: {{ rule.generation_rules.length }}</span
          >
        </div>
      </div>
    </CAccordionHeader>
    <CAccordionBody>
      <div class="d-flex justify-content-between align-items-center w-100 pb-2">
        <div>Rule Details:</div>
        <AdminRuleEnableForm :rule="props.rule" />
      </div>
      <pre class="bg-secondary ma-2 rounded text-white">{{
        JSON.stringify(rule, null, 2)
      }}</pre>
    </CAccordionBody>
  </CAccordionItem>
</template>
