<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import type { Artifact } from "@/api/types";
import {
  CAccordion,
  CAccordionBody,
  CAccordionHeader,
  CAccordionItem,
  CBadge,
  CListGroup,
  CListGroupItem,
} from "@coreui/bootstrap-vue";

const props = defineProps<{
  tracked: Artifact[];
}>();
const additional_filters_accordion_vars = {
  "--bs-accordion-btn-padding-x": "0.5rem",
  "--bs-accordion-btn-padding-y": "0.5rem",
  "--bs-accordion-bg": "transparent",
  "--bs-accordion-active-color": "var(--bs-body-color)",
  "--bs-accordion-active-bg": "transparent",
  "--bs-accordion-btn-focus-box-shadow": "none",
  "--bs-accordion-btn-focus-border-color": "none",
  "--bs-accordion-body-padding-x": 0,
  "--bs-accordion-body-padding-y": 0,
};
</script>

<template>
  <div class="mt-3">
    <!-- prevent the default action of click events on the accordion button, or it will submit the form -->
    <CAccordion
      flush
      :style="additional_filters_accordion_vars"
      @click.prevent=""
      class="bg-light border rounded"
    >
      <CAccordionItem :item-key="1">
        <CAccordionHeader>
          This Rule will track {{ props.tracked.length }} artifacts:
        </CAccordionHeader>
        <CAccordionBody>
          <CListGroup flush>
            <CListGroupItem
              v-for="artifact in props.tracked"
              :key="artifact.name"
              class="d-flex align-items-center justify-content-between"
            >
              {{ artifact.name }}
              <CBadge color="light" class="text-secondary border">{{
                artifact.type
              }}</CBadge>
            </CListGroupItem>
          </CListGroup>
        </CAccordionBody>
      </CAccordionItem>
    </CAccordion>
  </div>
</template>
