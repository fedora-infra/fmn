<script setup lang="ts">
import { CListGroupItem } from "@coreui/bootstrap-vue";
import { TRACKING_RULES } from "../api/constants";
import type { Rule } from "../api/types";
const props = defineProps<{
  rule: Rule;
}>();
defineEmits<{ (e: "change", value: string | null): void }>();
</script>

<template>
  <CListGroupItem
    class="d-flex d-flex justify-content-between align-items-center"
  >
    <div>
      <div class="fw-bold">{{ props.rule.name }}</div>
      <div>
        {{
          TRACKING_RULES.find((o) => o.name === props.rule.tracking_rule).label
        }}
      </div>
    </div>
    <div>
      <div>{{ rule.destinations }}</div>
      <div>{{ rule.filters }}</div>
    </div>
  </CListGroupItem>
</template>