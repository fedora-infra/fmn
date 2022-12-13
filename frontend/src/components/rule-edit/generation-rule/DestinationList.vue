<script setup lang="ts">
import { apiGet } from "@/api";
import type { Destination } from "@/api/types";
import { useUserStore } from "@/stores/user";
import type { QueryFunction } from "react-query/types/core";

const props = defineProps<{
  name?: string;
}>();

const userStore = useUserStore();
const apiGetDestinations = apiGet as QueryFunction<Destination[]>;
const url = `/api/v1/users/${userStore.username}/destinations`;

const getDestinations = async () => {
  type Option = { name: string; label: string; options: Destination[] };
  const data = await apiGetDestinations({
    queryKey: [url],
    meta: undefined,
  });
  const result: Option[] = [
    { name: "email", label: "Email", options: [] },
    { name: "irc", label: "IRC", options: [] },
    { name: "matrix", label: "Matrix", options: [] },
  ];
  (data || []).forEach((d: Destination) => {
    const group = result.filter((g) => g.name === d.protocol)[0];
    group.options.push(d);
  });
  return result;
};
</script>

<template>
  <div class="mb-4">
    <FormKit
      type="multiselect"
      :name="props.name || 'destinations'"
      mode="tags"
      :close-on-select="false"
      groups
      group-hide-empty
      :groupSelect="false"
      :msOptions="getDestinations"
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
