<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { useRuleQuery } from "@/api/rules";
import { CAlert, CSpinner } from "@coreui/bootstrap-vue";
import { useRoute } from "vue-router";
import RuleEditForm from "../components/RuleEditForm.vue";

const route = useRoute();
const { isLoading, isError, data, error } = useRuleQuery(
  parseInt(route.params.id as string),
);
</script>

<template>
  <div v-if="isLoading" class="text-center"><CSpinner /></div>
  <CAlert v-else-if="isError" color="danger">
    Could not load the rule: {{ error?.detail }}
  </CAlert>
  <RuleEditForm v-else-if="data" :rule="data" />
</template>
