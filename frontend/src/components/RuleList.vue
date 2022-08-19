<script setup lang="ts">
import { CListGroup, CListGroupItem } from "@coreui/bootstrap-vue";
import type { QueryFunction } from "react-query/types/core";
import { useQuery } from "vue-query";
import { apiGet } from "../api";
import type { Rule } from "../api/types";
import RuleListItem from "../components/RuleListItem.vue";
import { useUserStore } from "../stores/user";

const userStore = useUserStore();
const route = `/user/${userStore.username}/rules`;
const { isLoading, isError, data, error } = useQuery(
  route,
  apiGet as QueryFunction<Rule[]>
);
</script>

<template>
  <span v-if="isLoading">Loading...</span>
  <span v-else-if="isError">Error: {{ error }}</span>
  <template v-else>
    <CListGroup>
      <CListGroupItem
        class="d-flex justify-content-between align-items-center bg-light"
      >
        <span class="fw-bold">{{ data ? data.length : "?" }} rules </span>
        <router-link to="/rules/new" class="btn btn-primary">
          Add a new rule
        </router-link>
      </CListGroupItem>
      <RuleListItem v-for="rule in data" :key="rule.name" :rule="rule" />
    </CListGroup>
  </template>
</template>
