<script setup lang="ts">
import FilterApplication from "./FilterApplication.vue";
import FilterMyActions from "./FilterMyActions.vue";
import FilterSeverity from "./FilterSeverity.vue";
import FilterTopic from "./FilterTopic.vue";

/*
const filters = reactive({
  application: null,
  severity: null,
  my_actions: false,
  topic: null,
});

const handleChange = (key: string, value: string | boolean | null) => {
  filters[key] = value;
};
*/
</script>

<template>
  <FormKit type="group" name="filters">
    <FilterApplication />
    <FilterSeverity />
    <FilterMyActions />
    <FilterTopic />
  </FormKit>
</template>
