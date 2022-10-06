<script setup lang="ts">
import type { Artifact } from "@/api/types";
import {
  CAccordion,
  CAccordionBody,
  CAccordionHeader,
  CAccordionItem,
  CBadge,
} from "@coreui/bootstrap-vue";

const props = defineProps<{
  tracked: Artifact[];
}>();
const additional_filters_accordion_vars = {
  "--bs-accordion-btn-padding-x": 0,
  "--bs-accordion-btn-padding-y": 0,
  "--bs-accordion-bg": "transparent",
  "--bs-accordion-active-color": "var(--bs-body-color)",
  "--bs-accordion-active-bg": "transparent",
  "--bs-accordion-btn-focus-box-shadow": "none",
  "--bs-accordion-btn-focus-border-color": "none",
};
</script>

<template>
  <div class="mt-3">
    <!-- prevent the default action of click events on the accordion button, or it will submit the form -->
    <CAccordion
      flush
      :style="additional_filters_accordion_vars"
      @click.prevent=""
    >
      <CAccordionItem :item-key="1">
        <CAccordionHeader>
          This Rule will track {{ props.tracked.length }} artefacts:
        </CAccordionHeader>
        <CAccordionBody>
          <ul class="list-unstyled">
            <li v-for="artifact in props.tracked" :key="artifact.name">
              <CBadge color="info">{{ artifact.type }}</CBadge>
              {{ artifact.name }}
            </li>
          </ul>
        </CAccordionBody>
      </CAccordionItem>
    </CAccordion>
  </div>
</template>
