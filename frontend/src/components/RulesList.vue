<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { TRACKING_RULES } from "@/api/constants";
import type { Rule } from "@/api/types";
import { isDefined } from "@/util";
import {
  CCard,
  CCardBody,
  CListGroup,
  CListGroupItem,
} from "@coreui/bootstrap-vue";
import { computed, ref } from "vue";
import RuleListItem from "../components/RuleListItem.vue";

const props = defineProps<{
  rules: Rule[];
}>();

const tracking_rule_filter = ref("");
const filteringOptions = computed(() => {
  const options = [
    ...new Set(
      (props.rules || [])
        .map((rule) => rule.tracking_rule.name)
        .map((name) => TRACKING_RULES.find((tr) => tr.name === name))
        .filter(isDefined),
    ),
  ];
  return options.map((rule) => {
    return { value: rule.name, label: rule.label };
  });
});

const rules = computed(() =>
  [...props.rules]
    .filter(
      (r) =>
        !tracking_rule_filter.value ||
        r.tracking_rule.name.includes(tracking_rule_filter.value),
    )
    .sort(
      (a, b) =>
        Number(a.disabled) - Number(b.disabled) ||
        b.tracking_rule.name.localeCompare(a.tracking_rule.name),
    ),
);
</script>

<template>
  <div class="d-flex justify-content-between mb-3">
    <h1 class="mb-0">My Rules</h1>
    <router-link to="/rules/new" class="btn btn-primary"
      >Add a new rule</router-link
    >
  </div>
  <CCard v-if="rules.length === 0" class="border bg-light py-5">
    <CCardBody>
      <h2 class="text-center text-muted">No Rules.</h2>
      <div class="text-center mt-3">
        <router-link to="/rules/new" class="btn btn-primary">
          Create a Rule
        </router-link>
      </div>
    </CCardBody>
  </CCard>
  <template v-else>
    <CListGroup>
      <CListGroupItem class="bg-light d-flex align-items-center">
        <div class="fw-bold">
          {{ props.rules.length }} rule<template v-if="props.rules.length > 1"
            >s</template
          ><template v-if="props.rules.length !== rules.length"
            >, {{ rules.length }} shown</template
          >
        </div>
        <div class="fw-bold text-secondary ms-auto me-2">Filter by:</div>
        <div style="min-width: 220px">
          <FormKit
            type="multiselect"
            name="filter_tracking_rules"
            placeholder="Tracking Rule"
            :msOptions="filteringOptions"
            :close-on-select="true"
            :multiple="false"
            v-model="tracking_rule_filter"
          />
        </div>
      </CListGroupItem>
      <RuleListItem v-for="rule in rules" :key="rule.id" :rule="rule" />
    </CListGroup>
  </template>
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
