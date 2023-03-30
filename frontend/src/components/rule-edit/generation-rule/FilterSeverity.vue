<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<!-- eslint-disable prettier/prettier -->
<script setup lang="ts">
import { SEVERITIES } from "@/api/constants";
</script>

<template>
  <p class="mb-0 fw-bold">Severities:</p>
  <FormKit
    type="multiselect"
    name="severities"
    placeholder="Choose severities"
    mode="tags"
    :msOptions="SEVERITIES.map((s) => s.label)"
    :close-on-select="false"
  />
</template>
