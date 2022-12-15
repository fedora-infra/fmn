<script setup lang="ts">
import { CListGroupItem } from "@coreui/bootstrap-vue";
import { cilPen } from "@coreui/icons";
import { CIcon } from "@coreui/icons-vue";

import { TRACKING_RULES } from "../api/constants";

import type { Rule, TrackingRule } from "../api/types";
import DestinationTag from "./DestinationTag.vue";
const props = defineProps<{
  rule: Rule;
}>();

const tracking_rule = TRACKING_RULES.find(
  (o) => o.name === props.rule.tracking_rule.name
) as TrackingRule;
</script>

<template>
  <CListGroupItem
    class="d-flex justify-content-between align-items-center"
    :class="{ 'bg-light text-muted': props.rule.disabled }"
  >
    <div>
      <div class="fw-bold">{{ props.rule.name }}</div>
      <div>
        {{ tracking_rule.label }}
      </div>
    </div>
    <div>
      <template v-for="(gr, index) in rule.generation_rules" :key="index">
        <DestinationTag
          v-for="destination in gr.destinations"
          :destination="destination"
          :key="`${destination.protocol}:${destination.address}`"
        />
      </template>
      <div class="text-end">
        <template v-for="(gr, index) in rule.generation_rules" :key="index">
          <template v-for="(f_params, f_name) in gr.filters" :key="f_name">
            <span
              class="badge text-bg-warning fw-normal ms-1"
              v-if="
                f_params !== null &&
                f_params !== false &&
                !(Array.isArray(f_params) && f_params.length === 0)
              "
              ><strong>{{ f_name }}</strong>
              <template v-if="typeof f_params !== 'boolean'"> : </template>
              <template v-if="Array.isArray(f_params)">{{
                f_params.join(", ")
              }}</template
              ><template v-else-if="typeof f_params !== 'boolean'">{{
                f_params
              }}</template></span
            >
          </template>
        </template>
      </div>
    </div>
    <div>
      <router-link
        :to="`/rules/${props.rule.id}`"
        class="btn btn-outline-primary ms-1"
      >
        <CIcon :icon="cilPen" />
      </router-link>
    </div>
  </CListGroupItem>
</template>
