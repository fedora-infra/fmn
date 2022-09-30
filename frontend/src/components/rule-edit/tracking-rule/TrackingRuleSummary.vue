<script setup lang="ts">
import {
  CAccordion,
  CAccordionBody,
  CAccordionHeader,
  CAccordionItem,
} from "@coreui/bootstrap-vue";

const props = defineProps<{
  tracked: string[];
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
    <CAccordion flush :style="additional_filters_accordion_vars">
      <CAccordionItem :item-key="1">
        <CAccordionHeader>
          This Rule will track {{ props.tracked.length }} artefacts:
        </CAccordionHeader>
        <CAccordionBody>
          <ul class="list-unstyled">
            <li v-for="artifact in props.tracked" :key="artifact">
              {{ artifact }}
            </li>
          </ul>
        </CAccordionBody>
      </CAccordionItem>
    </CAccordion>
  </div>
</template>
