<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import {
  CAlert,
  CAlertHeading,
  CAlertLink,
  CSpinner,
} from "@coreui/bootstrap-vue";
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
const router = useRouter();
const route = useRoute();
const routerIsReady = computed(
  () =>
    // Authentication callback routes are added after the initial routing has happened, ignore them.
    route.path.slice(0, 7) !== "/login/",
);
</script>

<template>
  <CAlert color="warning" v-if="routerIsReady">
    <CAlertHeading>Page not found.</CAlertHeading>
    <p>
      If you followed a link here, please
      <CAlertLink href="#" @click="() => router.back()">go back</CAlertLink> and
      report the broken link to the webmaster.
    </p>
  </CAlert>
  <div v-else class="text-center"><CSpinner /></div>
</template>
