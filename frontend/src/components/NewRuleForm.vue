<script setup lang="ts">
import { CButton } from "@coreui/bootstrap-vue";
import { FormKit } from "@formkit/vue";
import DestinationList from "./DestinationList.vue";
import FilterList from "./FilterList.vue";
import TrackingRuleList from "./TrackingRuleList.vue";

const handleSubmit = async (val: any) => {
  console.log("Will submit the new rule:", val);
};
</script>

<template>
  <FormKit type="form" id="new-rule" :actions="false" @submit="handleSubmit">
    <div class="mb-3">
      <FormKit name="name" type="text" placeholder="Rule name" />
    </div>
    <div class="mb-3">
      <TrackingRuleList />
    </div>

    <div class="mb-3">
      <DestinationList />
    </div>

    <div class="mb-3">
      <p>Choose a filter if you want:</p>
      <FilterList />
    </div>

    <CButton type="submit" color="primary">Create Rule</CButton>
  </FormKit>
</template>
