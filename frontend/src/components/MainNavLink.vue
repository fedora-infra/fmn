<template>
  <li class="nav-item">
    <router-link v-bind="$attrs" class="nav-link"><slot /></router-link>
  </li>
</template>

<script lang="ts">
export default {
  inheritAttrs: false,
};
</script>
