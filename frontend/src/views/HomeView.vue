<script setup lang="ts">
import { useQuery } from "vue-query";
import { apiGet } from "../api";

const { isLoading, isError, data, error } = useQuery("", apiGet);
</script>

<template>
  <div class="p-5 mb-4">
    <div class="home">
      <h1 class="fw-bold display-5">Notifications</h1>
      <p class="col-md-8 fs-4">
        Centrally managed preferences for Fedora Infrastructure notifications to
        your inbox, irc client, and mobile device.
      </p>
    </div>
  </div>
  <div class="mt-5">
    <p>Result of an API call to <code>/</code>:</p>
    <p>
      <span v-if="isLoading">Loading...</span>
      <span v-else-if="isError">Error: {{ error }}</span>
      <!-- We can assume by this point that `isSuccess === true` -->
      <code v-else>{{ data }}</code>
    </p>
  </div>
</template>

<style></style>
