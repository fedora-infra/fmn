<template>
  <li class="nav-item">
    <router-link v-bind="props" class="nav-link"><slot /></router-link>
  </li>
</template>

<script setup lang="ts">
import type { RouterLinkProps } from "vue-router";
// The defineProps extractor can't currently use complex types such as RouterLinkProps directly
// https://github.com/wheatjs/vite-plugin-vue-type-imports/issues/28
const props = defineProps<{ to: RouterLinkProps["to"] }>();
</script>
