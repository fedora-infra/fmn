<template>
  <p v-if="userStore.username">
    Authenticated as {{ userStore.fullName }} ({{ userStore.username }}),
    redirecting...
  </p>
  <p v-else-if="loading">Loading user information...</p>
  <p v-else-if="error">{{ error }}</p>
  <p v-else>Authentication successful, redirecting you back...</p>
</template>

<script setup lang="ts">
import { useToastStore } from "@/stores/toast";
import { onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../auth";
import { useUserStore } from "../stores/user";

const auth = useAuth();
const router = useRouter();
const userStore = useUserStore();
const toastStore = useToastStore();
const loading = ref(true);
const error = ref<string | null>(null);

onMounted(async () => {
  if (!auth) {
    return;
  }
  await auth.fetchServiceConfiguration();
  try {
    await auth.handleAuthorizationRedirect((result) => {
      userStore.importTokenResponse(result);
      auth.makeUserInfoRequest(result.accessToken).then((userinfo) => {
        userStore.importUserInfoResponse(userinfo);
      });
      return result;
    });
  } catch (err) {
    error.value = err as string;
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
    let redirectTo = sessionStorage.getItem("redirect_to");
    if (!redirectTo || redirectTo.match(/^\/login.*/)) {
      redirectTo = "/";
    }
    sessionStorage.removeItem("redirect_to");
    toastStore.addToast({
      color: "success",
      title: "Login successful!",
      content: `Welcome, ${userStore.fullName}.`,
    });

    console.log("Will redirect to", redirectTo);
    router.push(redirectTo);
  }
);
</script>
