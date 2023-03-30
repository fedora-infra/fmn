<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<template>
  <CToaster placement="top-center">
    <CToast
      v-for="toast in toasts"
      :key="toast.id"
      :color="toast.color"
      class="text-white"
    >
      <CToastHeader closeButton v-if="toast.title">
        <span class="me-auto fw-bold">{{ toast.title }}</span>
        <small>{{ $d(toast.date, "short") }}</small>
      </CToastHeader>
      <CToastBody>{{ toast.content }}</CToastBody>
      <CToastClose class="me-2 m-auto" v-if="!toast.title" />
    </CToast>
  </CToaster>
</template>

<script setup lang="ts">
import {
  CToast,
  CToastBody,
  CToastClose,
  CToaster,
  CToastHeader,
} from "@coreui/bootstrap-vue";
import { useToastStore } from "../stores/toast";

const toastStore = useToastStore();
const toasts = toastStore.toasts;
</script>
