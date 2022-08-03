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
        <li><a class="dropdown-item" @click.prevent="doLogout">Logout</a></li>
      </ul>
    </template>
    <a v-else @click.prevent="doLogin()" href="#" class="nav-link">Login</a>
  </li>
</template>

<script setup lang="ts">
import { useUserStore } from "@/stores/user";
import { useRoute, useRouter } from "vue-router";
import { login, logout, useAuth } from "../auth";

const auth = useAuth();
const route = useRoute();
const userStore = useUserStore();
const router = useRouter();

const doLogin = () => login(auth, route.fullPath);

const doLogout = () => {
  logout();
  if (route.meta.auth) {
    router.push("/");
  }
};
</script>
