<script setup lang="ts">
import { onMounted, watch } from "vue";
import { useI18n } from "vue-i18n";
import { RouterView } from "vue-router";
import PageFooter from "./components/PageFooter.vue";
import PageHeader from "./components/PageHeader.vue";
import { setLocale } from "./i18n";

const i18n = useI18n();
// Reset the locale when new components are loaded and new languages become available
onMounted(() => {
  setLocale(i18n);
});
watch(i18n.messages, (oldValue, newValue) => {
  if (Object.keys(oldValue) === Object.keys(newValue)) {
    return;
  }
  setLocale(i18n);
});
</script>

<template>
  <PageHeader />
  <div class="container py-5">
    <RouterView />
  </div>
  <PageFooter />
</template>
