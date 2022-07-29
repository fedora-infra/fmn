<script setup lang="ts">
import axios from "axios";
import { useQuery } from "vue-query";

const showJSON = async () => {
  const response = await axios.get(import.meta.env.VITE_API_URL);
  console.log(response);
  return response.data;
};
const { isLoading, isError, data, error } = useQuery("root", showJSON);
</script>

<template>
  <div class="about">
    <h1>This is the home page</h1>
  </div>
  <p>Result of an API call to <code>/</code>:</p>
  <p>
    <span v-if="isLoading">Loading...</span>
    <span v-else-if="isError">Error: {{ error }}</span>
    <!-- We can assume by this point that `isSuccess === true` -->
    <code v-else>{{ data }}</code>
  </p>
</template>

<style></style>
