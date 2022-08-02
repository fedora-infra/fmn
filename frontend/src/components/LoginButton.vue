<template>
  <li class="nav-item" :class="{ dropdown: userStore.loggedIn }">
    <template v-if="userStore.loggedIn">
      <a
        class="nav-link dropdown-toggle"
        href="#"
        ole="button"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        {{ userStore.fullName }}
      </a>
      <ul class="dropdown-menu">
        <li><a class="dropdown-item" @click.prevent="logout">Logout</a></li>
      </ul>
    </template>
    <button v-else @click="login()" class="btn btn-link nav-link">Login</button>
  </li>
</template>

<script setup lang="ts">
import { useUserStore } from "@/stores/user";
import { useRoute } from "vue-router";
import { scope, useAuth } from "../auth";
const auth = useAuth();
const route = useRoute();
const userStore = useUserStore();

const login = async () => {
  if (!auth) {
    return;
  }
  // Store where we clicked the button
  localStorage.setItem("redirect_to", route.fullPath);
  // Get the URLs from Ipsilon
  try {
    await auth.fetchServiceConfiguration();
  } catch (err) {
    console.log(err);
    // TODO: Ewww. Use flash messages or snackbar
    alert("Could not connect to Ipsilon: " + err);
  }
  // Start the authentication dance
  await auth.makeAuthorizationRequest(scope);
};
const logout = () => {
  userStore.logout();
};
</script>
