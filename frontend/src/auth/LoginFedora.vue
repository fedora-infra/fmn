<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<template>
  <p v-if="userStore.username">
    Authenticated as {{ userStore.fullName }} ({{ userStore.username }}),
    redirecting...
    <CSpinner size="sm" />
  </p>
  <CAlert v-else-if="error" color="danger">
    <CAlertHeading>Login failed!</CAlertHeading>
    {{ error }}
  </CAlert>
  <p v-else-if="loading">
    Loading user information...
    <CSpinner size="sm" />
  </p>
  <p v-else>Authentication successful, redirecting you back...</p>
</template>

<script setup lang="ts">
import { getApiClient } from "@/api";
import type { APIError, User } from "@/api/types";
import { useToastStore } from "@/stores/toast";
import { CAlert, CAlertHeading, CSpinner } from "@coreui/bootstrap-vue";
import { onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from ".";
import { useUserStore } from "../stores/user";

const auth = useAuth();
const router = useRouter();
const userStore = useUserStore();
const toastStore = useToastStore();
const loading = ref(true);
const error = ref<string | null>(null);

const getRedirect = () => {
  let redirectTo = sessionStorage.getItem("redirect_to");
  if (!redirectTo || redirectTo.match(/^\/login.*/)) {
    redirectTo = "/";
  }
  sessionStorage.removeItem("redirect_to");
  return redirectTo;
};

onMounted(async () => {
  if (!auth) {
    return;
  }
  if (userStore.loggedIn) {
    const redirectTo = getRedirect();
    console.log("User already logged in, redirecting to", redirectTo);
    router.push(redirectTo);
  }
  await auth.fetchServiceConfiguration();
  try {
    const result = await auth.handleAuthorizationRedirect();
    userStore.importTokenResponse(result);
    const userInfo = await auth.makeUserInfoRequest(result.accessToken);
    const apiClient = await getApiClient();
    const url = "/api/v1/users/me";
    try {
      const response = await apiClient.get<User>(url);
      userStore.setAdmin(response.data.is_admin || false);
      // Only import the userinfo response if the API answered.
      userStore.importUserInfoResponse(userInfo);
    } catch (e) {
      const error = e as APIError;
      throw `Could not retrieve user information from the API: ${
        error.response?.data?.detail || error.message
      }.`;
    }
  } catch (err) {
    console.error(err);
    userStore.logout();
    error.value = err as string;
    loading.value = false;
  }
});

watch(
  () => userStore.username,
  (value) => {
    if (!value) {
      return;
    }
    loading.value = false;
    // TODO: handle errors
    const redirectTo = getRedirect();
    toastStore.addToast({
      color: "success",
      title: "Login successful!",
      content: `Welcome, ${userStore.fullName}.`,
    });

    console.log("Will redirect to", redirectTo);
    router.push(redirectTo);
  },
);
</script>
