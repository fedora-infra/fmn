<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { CListGroupItem } from "@coreui/bootstrap-vue";

import { TRACKING_RULES } from "../api/constants";

import type { Rule } from "../api/types";
import DestinationTag from "./DestinationTag.vue";
import RuleListItemTitle from "./RuleListItemTitle.vue";

const props = defineProps<{
  rule: Rule;
}>();

const tracking_rule = TRACKING_RULES.find(
  (o) => o.name === props.rule.tracking_rule.name,
);
</script>

<template>
  <CListGroupItem
    class="d-flex justify-content-between align-items-center"
    :class="{ 'text-muted bg-light': props.rule.disabled }"
    style="--bs-bg-opacity: 0.4"
    v-if="tracking_rule"
  >
    <div class="text-truncate pb-1">
      <div class="fw-bold">
        <RuleListItemTitle :rule="rule" />
      </div>
      <div class="d-flex align-items-center">
        <span
          class="me-2 badge border text-secondary border-success bg-success"
          style="padding-top: 7px; padding-bottom: 7px; --bs-bg-opacity: 0.1"
          >{{ tracking_rule.label }}</span
        >
        <template v-for="(gr, index) in rule.generation_rules" :key="index">
          <DestinationTag
            v-for="destination in gr.destinations"
            :destination="destination"
            :icononly="true"
            :key="`${destination.protocol}:${destination.address}`"
          />
        </template>
      </div>
    </div>
    <div
      class="badge rounded-pill bg-light border fs-5 text-secondary"
      v-c-tooltip="'messages in the last 7 days'"
    >
      {{ rule.generated_last_week }}
    </div>
  </CListGroupItem>
</template>
