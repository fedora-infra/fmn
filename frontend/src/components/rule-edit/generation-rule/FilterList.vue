<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { CCol, CRow } from "@coreui/bootstrap-vue";
import FilterApplication from "./FilterApplication.vue";
import FilterMyActions from "./FilterMyActions.vue";
import FilterSeverity from "./FilterSeverity.vue";
import FilterTopic from "./FilterTopic.vue";

/*
const filters = reactive({
  applications: [],
  severities: [],
  my_actions: false,
  topic: null,
});

const handleChange = (key: string, value: string | boolean | null) => {
  filters[key] = value;
};
*/

const props = defineProps<{
  name?: string;
}>();
</script>

<template>
  <h4>Optional Filters</h4>
  <FormKit type="group" :name="props.name || 'filters'">
    <CRow :xs="{ gutter: 3 }">
      <CCol xs="12" sm="6">
        <FilterSeverity />
      </CCol>
      <CCol xs="12" sm="6">
        <FilterApplication />
      </CCol>
      <CCol xs="12" sm="6">
        <FilterMyActions />
      </CCol>
      <CCol xs="12" sm="6">
        <FilterTopic />
      </CCol>
    </CRow>
  </FormKit>
</template>
