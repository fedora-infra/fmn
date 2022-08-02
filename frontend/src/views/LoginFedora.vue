<template>
  <p v-if="userStore.username">
    Already authenticated as {{ userStore.fullName }} ({{ userStore.username }})
  </p>
  <p v-else-if="loading">Loading...</p>
  <p v-else-if="error">{{ error }}</p>
  <p v-else>Authentication successful, redirecting you back...</p>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../auth";
import { useUserStore } from "../stores/user";

const auth = useAuth();
const router = useRouter();
const userStore = useUserStore();
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
    let redirectTo = localStorage.getItem("redirect_to");
    if (!redirectTo || redirectTo.match(/^\/login.*/)) {
      redirectTo = "/";
    }
    localStorage.removeItem("redirect_to");
    // TODO: add a flash message
    console.log("Will redirect to", redirectTo);
    router.push(redirectTo);
  }
);
</script>
