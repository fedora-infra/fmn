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
  <span v-if="isLoading">Loading...</span>
  <span v-else-if="isError">Error: {{ error }}</span>
  <!-- We can assume by this point that `isSuccess === true` -->
  <div v-else>
    <div v-for="destination in data" :key="destination.name" class="form-check">
      <input
        class="form-check-input"
        type="checkbox"
        :name="`destination-${destination.name}`"
        value=""
        :id="`destination-${destination.name}`"
        :disabled="destination.values.length === 0"
      />
      <label class="form-check-label" :for="`destination-${destination.name}`">
        {{ destination.title }}:
        <select
          :name="`destination-${destination.name}-value`"
          v-if="destination.values.length !== 0"
        >
          <option
            v-for="value in destination.values"
            :key="value"
            :value="value"
          >
            {{ value }}
          </option>
        </select>
        <span v-else
          >no value, go to
          <a href="https://accounts.fedoraproject.org">Fedora accounts</a> to
          set it</span
        >
      </label>
    </div>
  </div>
</template>
