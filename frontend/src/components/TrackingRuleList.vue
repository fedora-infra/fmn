<script setup lang="ts">
import type { QueryFunction } from "react-query/types/core";
import { useQuery } from "vue-query";
import { apiGet } from "../api";
import type { TrackingRule } from "../api/types";

const route = "/rules";
const { isLoading, isError, data, error } = useQuery(
  route,
  apiGet as QueryFunction<TrackingRule[]>
);
</script>

<template>
  <span v-if="isLoading">Loading...</span>
  <span v-else-if="isError">Error: {{ error }}</span>
  <!-- We can assume by this point that `isSuccess === true` -->
  <div v-else>
    <div v-for="rule in data" :key="rule.name" class="form-check">
      <input
        class="form-check-input"
        type="radio"
        name="trackingrule"
        :id="`trackingrule-${rule.name}`"
        :value="rule.name"
      />
      <label class="form-check-label" :for="`trackingrule-${rule.name}`">
        {{ rule.title }}
      </label>
    </div>
  </div>
</template>
