<script setup lang="ts">
import { apiGet } from "@/api";
import type { Destination } from "@/api/types";
import { useUserStore } from "@/stores/user";
import type { QueryFunction } from "react-query/types/core";
import { computed } from "vue";
import { useQuery } from "vue-query";

const props = defineProps<{
  name?: string;
}>();

const userStore = useUserStore();
const route = `/user/${userStore.username}/destinations`;
const { isLoading, isError, data, error } = useQuery(
  route,
  apiGet as QueryFunction<Destination[]>
);
type Option = { name: string; label: string; options: Destination[] };
const options = computed(() => {
  const result: Option[] = [
    { name: "email", label: "Email", options: [] },
    { name: "irc", label: "IRC", options: [] },
    { name: "matrix", label: "Matrix", options: [] },
  ];
  (data.value || []).forEach((d: Destination) => {
    const group = result.filter((g) => g.name === d.protocol)[0];
    group.options.push(d);
  });
  return result;
});
</script>

<template>
  <span v-if="isLoading"
    ><input
      type="text"
      class="form-control"
      disabled
      value="Loading destinations..."
  /></span>
  <span v-else-if="isError">Error: {{ error }}</span>
  <!-- We can assume by this point that `isSuccess === true` -->
  <div v-else class="mb-4">
    <FormKit
      type="multiselect"
      :name="props.name || 'destinations'"
      mode="tags"
      :close-on-select="false"
      groups
      group-hide-empty
      :groupSelect="false"
      :msOptions="options"
      label="Destinations:"
      label-class="fw-bold"
      msLabel="address"
      valueProp="address"
      object
      placeholder="Select where you want the messages to go"
      validation="required"
    />
  </div>
</template>
