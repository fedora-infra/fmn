<script setup lang="ts">
import { TRACKING_RULES } from "@/api/constants";
import type { Rule, TrackingRule } from "@/api/types";
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
const filteringOptions = computed(() => [
  ...new Set(
    (props.rules || [])
      .map((rule) => rule.tracking_rule.name)
      .map((name) => TRACKING_RULES.find((tr) => tr.name === name))
      .filter((o) => typeof o !== "undefined") as TrackingRule[]
  ),
]);
</script>

<template>
  <CCard v-if="props.rules.length === 0" class="border bg-light py-5">
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
    <p class="fw-bold">{{ props.rules.length }} rule(s)</p>

    <CListGroup>
      <CListGroupItem
        class="d-flex justify-content-between align-items-center bg-light"
      >
        <select name="filter_tracking_rules" v-model="tracking_rule_filter">
          <option value="">All</option>
          <option
            v-for="option in filteringOptions"
            :value="option.name"
            :key="option.name"
          >
            {{ option.label }}
          </option>
        </select>
        <router-link to="/rules/new" class="btn btn-primary">
          Add a new rule
        </router-link>
      </CListGroupItem>
      <RuleListItem
        v-for="rule in props.rules.filter(
          (r) =>
            !tracking_rule_filter ||
            r.tracking_rule.name.includes(tracking_rule_filter)
        )"
        :key="rule.id"
        :rule="rule"
      />
    </CListGroup>
  </template>
</template>
