<script setup lang="ts">
import { usePreviewRuleQuery } from "@/api/rules";
import type { Rule } from "@/api/types";
import { CListGroup, CListGroupItem, CSpinner } from "@coreui/bootstrap-vue";
import { formatRelative } from "date-fns";
import { enUS } from "date-fns/locale";

const props = defineProps<{
  data: Omit<Rule, "id">;
}>();

const { isLoading, isError, data, error } = usePreviewRuleQuery(props.data);
</script>

<template>
  <div v-if="isLoading" class="text-center">
    <p>
      Loading a preview of the notifications that would be produced by this
      rule…
    </p>
    <CSpinner />
  </div>
  <p v-if="isError">Error: {{ error }}</p>
  <CListGroup v-if="data">
    <CListGroupItem class="text-center fw-bold bg-light">
      {{ data.length }} messages matched in the past 24 hours
    </CListGroupItem>
    <CListGroupItem v-for="notif in data" :key="notif.content.date">
      <div class="d-flex justify-content-between align-items-center">
        <div class="fw-bold">{{ notif.content.summary }}</div>
        <div>
          <small>{{
            formatRelative(new Date(notif.content.date), new Date(), {
              locale: enUS,
            })
          }}</small>
        </div>
      </div>
      <div>
        <span class="badge bg-primary me-2" v-if="notif.content.application">
          Application: {{ notif.content.application }}
        </span>
        <span class="badge bg-secondary me-2" v-if="notif.content.topic">
          Topic: {{ notif.content.topic }}
        </span>
        <span class="badge bg-info me-2" v-if="notif.content.priority">
          Priority: {{ notif.content.priority }}
        </span>
      </div>
    </CListGroupItem>
  </CListGroup>
</template>
