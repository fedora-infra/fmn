<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import BaseFilterApplication from "./BaseFilterApplication.vue";
</script>

<template>
  <BaseFilterApplication
    name="applications"
    label="Applications"
    placeholder="Choose applications"
    help="If you leave this field empty, the rule applies to all applications (including new ones added later)"
  />
</template>
