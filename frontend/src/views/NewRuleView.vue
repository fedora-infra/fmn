<script setup lang="ts">
import DestinationList from "../components/DestinationList.vue";
import FilterList from "../components/FilterList.vue";
import TrackingRuleList from "../components/TrackingRuleList.vue";
</script>

<template>
  <div class="rules">
    <h1>Add a New Rule</h1>
    <form>
      <div class="mb-3">
        <p>Choose a tracking rule:</p>
        <TrackingRuleList />
      </div>

      <div class="mb-3">
        <p>Choose a destination:</p>
        <DestinationList />
      </div>

      <div class="mb-3">
        <p>Choose a filter if you want:</p>
        <FilterList />
      </div>
    </form>
  </div>
</template>
