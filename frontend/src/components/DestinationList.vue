<script setup lang="ts">
import type { QueryFunction } from "react-query/types/core";
import { useQuery } from "vue-query";
import { apiGet } from "../api";
import type { Destination } from "../api/types";
import { useUserStore } from "../stores/user";

const userStore = useUserStore();
const route = `/user/${userStore.username}/destinations`;
const { isLoading, isError, data, error } = useQuery(
  route,
  apiGet as QueryFunction<Destination[]>
);
</script>

<template>
  <span v-if="isLoading"
    ><input
      type="text"
      class="form-control"
      disabled
      value="Loading destinations..."
  /></span>
  <span v-else-if="isError">Error: {{ error }}</span>
  <!-- We can assume by this point that `isSuccess === true` -->
  <div v-else>
    <FormKit
      type="multiselect"
      name="destinations"
      mode="tags"
      :close-on-select="false"
      groups
      group-hide-empty
      :msOptions="data"
      placeholder="Choose one or more Destinations"
      validation="required"
    />
  </div>
</template>
