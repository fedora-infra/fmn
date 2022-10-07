<script setup lang="ts">
import { apiGet } from "@/api";
import type { User } from "@/api/types";
import type { QueryFunction } from "react-query/types/core";
import { ref } from "vue";

const value = ref<string[]>([]);
const apiGetUsers = apiGet as QueryFunction<{ users: User[] }>;
const route = "/users/";
const getUsers = async (query: string) => {
  const results = await apiGetUsers({
    queryKey: [route, { search: query }],
    meta: undefined,
  });
  return results ? results.users.map((u) => u.name) : [];
};
</script>

<template>
  <FormKit
    type="multiselect"
    name="params"
    label="Users:"
    label-class="fw-bold"
    placeholder="Search for users by username"
    mode="tags"
    v-model="value"
    :msOptions="getUsers"
    :close-on-select="false"
    searchable
    :filter-results="false"
    :resolve-on-load="false"
    validation="required"
    :min-chars="3"
    :delay="0"
  />
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
