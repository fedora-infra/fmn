<script setup lang="ts">
import type { QueryFunction } from "react-query/types/core";
import { useQuery } from "vue-query";
import { apiGet } from "../api";
import type { Filter } from "../api/types";

const route = "/filters";
const { isLoading, isError, data, error } = useQuery(
  route,
  apiGet as QueryFunction<Filter[]>
);
</script>

<template>
  <span v-if="isLoading">Loading...</span>
  <span v-else-if="isError">Error: {{ error }}</span>
  <!-- We can assume by this point that `isSuccess === true` -->
  <div v-else>
    <div v-for="filter in data" :key="filter.name" class="form-check">
      <input
        class="form-check-input"
        type="checkbox"
        :name="`filter-${filter.name}`"
        value=""
        :id="`filter-${filter.name}`"
      />
      <label class="form-check-label" :for="`filter-${filter.name}`">
        {{ filter.title }}
        <select v-if="filter.choices" :name="`filter-${filter.name}-value`">
          <option v-for="value in filter.choices" :key="value" :value="value">
            {{ value }}
          </option>
        </select>
        <input v-if="filter.str_arg" :name="`filter-${filter.name}-arg`" />
      </label>
    </div>
  </div>
</template>
