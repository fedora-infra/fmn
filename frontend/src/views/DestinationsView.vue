<script setup lang="ts">
import { useQuery } from "vue-query";
import { apiGet } from "../api";
import { useUserStore } from "../stores/user";

const userStore = useUserStore();
const route = `/userinfo/${userStore.username}`;
const { isLoading, isError, data, error } = useQuery(route, apiGet);
</script>

<template>
  <div>
    <h1>This is the destinations page</h1>
    <p>
      Result of an API call to <code>{{ route }}</code
      >:
    </p>
    <p>
      <span v-if="isLoading">Loading...</span>
      <span v-else-if="isError">Error: {{ error }}</span>
      <!-- We can assume by this point that `isSuccess === true` -->
      <code v-else>{{ data }}</code>
    </p>
  </div>
</template>
