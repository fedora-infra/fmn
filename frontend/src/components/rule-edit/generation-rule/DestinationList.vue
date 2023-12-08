<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { apiGet } from "@/api";
import type { Destination } from "@/api/types";
import { useUserStore } from "@/stores/user";
import type { AxiosError } from "axios";
import { ref } from "vue";

const props = defineProps<{
  name?: string;
}>();

type Option = { name: string; label: string; options: Destination[] };

const userStore = useUserStore();
const errors = ref<string[]>([]);
const url = `/api/v1/users/${userStore.username}/destinations`;

const getDestinations = async () => {
  errors.value = [];
  let data: Destination[];
  try {
    data = await apiGet<Destination[]>({
      queryKey: [url],
    });
  } catch (e) {
    const error = e as AxiosError;
    console.error(error.message);
    errors.value = [
      "Unable to get the available destinations, please try again later.",
    ];
    return [];
  }
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
const FAS_URL = `${import.meta.env.VITE_FAS}/user/${
  userStore.username
}/settings/profile/`;
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
      :errors="errors"
      :disabled="errors.length > 0"
    >
      <template #help>
        <small class="text-secondary">
          The destinations can be configured in the
          <a target="_blank" :href="FAS_URL">Fedora Account System</a>.
        </small>
      </template>
    </FormKit>
  </div>
</template>
