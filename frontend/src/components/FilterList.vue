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
    <div class="mb-2">
      <FilterApplication />
    </div>
    <div class="mb-2">
      <FilterSeverity />
    </div>
    <div class="mb-2">
      <FilterMyActions />
    </div>
    <div class="mb-2">
      <FilterTopic />
    </div>
  </FormKit>
</template>
