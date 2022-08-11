<script setup lang="ts">
import { RouterView } from "vue-router";
import PageFooter from "./components/PageFooter.vue";
import PageHeader from "./components/PageHeader.vue";
</script>

<template>
  <PageHeader />
  <div class="container py-5">
    <RouterView />
  </div>
  <PageFooter />
</template>
