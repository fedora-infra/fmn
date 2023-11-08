<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { apiGet } from "@/api";
import type { User } from "@/api/types";
// import type { QueryFunction } from "@tanstack/query-core/types";
import { ref } from "vue";
import AdminUserRulesList from "./AdminUserRulesList.vue";

//const apiGetUsers = apiGet as QueryFunction<User[]>;

const getUsers = async (query: string) => {
  if (!query) {
    return [];
  }
  // const results = await apiGetUsers({
  const results = await apiGet<User[]>({
    queryKey: ["/api/v1/admin/users", { search: query }],
  });
  const options = results.map((item) => item.name);
  return options;
};

const selectedUsername = ref("");

const handleChange = async (data: string) => {
  selectedUsername.value = data;
};
</script>

<template>
  <div
    class="d-flex justify-content-between align-items-center w-100 bg-light border rounded-top py-3 px-3"
  >
    <div class="w-25">
      <FormKit
        type="multiselect"
        name="name"
        placeholder="Search for User"
        :msOptions="getUsers"
        searchable
        :close-on-select="true"
        :multiple="false"
        track-by="name"
        :filter-results="false"
        :resolve-on-load="true"
        :min-chars="1"
        :delay="0"
        @input="handleChange"
      />
    </div>
  </div>
  <AdminUserRulesList v-if="selectedUsername" :username="selectedUsername" />
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
