<script setup lang="ts">
const api_docs_url = import.meta.env.VITE_API_URL + "/docs";
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
    <p>View online API docs <a :href="api_docs_url">here</a>.</p>
  </div>
</template>

<style></style>
