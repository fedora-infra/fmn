<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { TRACKING_RULES } from "../api/constants";
import type { Rule } from "../api/types";

const props = defineProps<{
  rule: Rule;
}>();

const tracking_rule = TRACKING_RULES.find(
  (o) => o.name === props.rule.tracking_rule.name,
);
</script>

<template>
  <router-link
    :to="`/rules/${props.rule.id}`"
    class="text-decoration-none"
    v-if="tracking_rule"
  >
    <span v-if="props.rule.name">{{ props.rule.name }}</span>
    <template v-else>
      {{ tracking_rule.prefixlabel
      }}<template
        v-if="rule.tracking_rule.params && rule.tracking_rule.params.length > 1"
        >s:</template
      ><template
        v-else-if="
          rule.tracking_rule.params && rule.tracking_rule.params.length == 1
        "
        >:</template
      >
      <template
        v-if="
          rule.tracking_rule.name == 'artifacts-owned' ||
          rule.tracking_rule.name == 'artifacts-group-owned' ||
          rule.tracking_rule.name == 'users-followed'
        "
      >
        <template
          v-for="(name, index) in rule.tracking_rule.params"
          :key="index"
          ><span v-if="index != 0">, </span
          ><strong>&#32;{{ name }}</strong></template
        >
      </template>
      <template v-if="rule.tracking_rule.name == 'artifacts-followed'">
        <template
          v-for="(artifact, index) in rule.tracking_rule.params"
          :key="index"
          ><span v-if="index != 0">,</span>
          <strong>{{ artifact.type }}/{{ artifact.name }}</strong></template
        >
      </template>
    </template>
  </router-link>
</template>
