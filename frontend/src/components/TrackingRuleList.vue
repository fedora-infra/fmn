<script setup lang="ts">
import type { QueryFunction } from "react-query/types/core";
import { useQuery } from "vue-query";
import { apiGet } from "../api";
import type { TrackingRule } from "../api/types";
import Multiselect from '@vueform/multiselect'


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
    <Multiselect
      v-model="value"
      placeholder="Choose a Tracking Rule"
      :options="data"
      searchable = true
    >
      <template v-slot:option="{ option }">
      <div>
        <strong>{{ option.label }}</strong>
        <div>{{option.description}} </div>
      </div>
      </template>
    </Multiselect>
  </div>
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
