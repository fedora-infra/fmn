<script setup lang="ts">
import { CButton } from "@coreui/bootstrap-vue";
import { FormKit } from "@formkit/vue";
import DestinationList from "./DestinationList.vue";
import FilterList from "./FilterList.vue";
import TrackingRuleList from "./TrackingRuleList.vue";

/* eslint-disable */
// warning  Unexpected any. Specify a different type  @typescript-eslint/no-explicit-any
const handleSubmit = async (val: any) => {
  console.log("Will submit the new rule:", val);
};
/* eslint-enable */
</script>

<template>
  <FormKit type="form" id="new-rule" @submit="handleSubmit" :actions="false">
    <div class="mb-3">
      <FormKit
        name="name"
        type="text"
        placeholder="Rule name"
        help="Choose a name for your new Rule"
        validation="required"
      />
    </div>
    <div class="mb-3">
      <TrackingRuleList />
    </div>

    <div class="mb-3">
      <DestinationList />
    </div>

    <div class="mb-3">
      <h4>Choose a filter (optional)</h4>
      <FilterList />
    </div>

    <div class="my-3">
      <CButton type="submit" color="primary">Create Rule</CButton>
    </div>
  </FormKit>
</template>
