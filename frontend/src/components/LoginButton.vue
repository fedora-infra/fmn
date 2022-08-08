<template>
  <li class="nav-item" :class="{ dropdown: userStore.loggedIn }">
    <template v-if="userStore.loggedIn">
      <a
        class="nav-link dropdown-toggle"
        href="#"
        role="button"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        <img v-bind:src="avatarURL" /> 
      </a>
      <ul class="dropdown-menu dropdown-menu-end">
        <li><a class="dropdown-item" @click.prevent="doLogout">Logout</a></li>
      </ul>
    </template>
    <a v-else @click.prevent="doLogin()" href="#" class="btn btn-primary">Login</a>
  </li>
</template>

<script setup lang="ts">
import { useUserStore } from "@/stores/user";
import { generateLibravatarURL } from "../util";
import { useRoute, useRouter } from "vue-router";
import { login, logout, useAuth } from "../auth";

const auth = useAuth();
const route = useRoute();
const userStore = useUserStore();
const router = useRouter();
const avatarURL = generateLibravatarURL("rlerch@redhat.com", 30, "retro");

const doLogin = () => login(auth, route.fullPath);

const doLogout = () => {
  logout();
  if (route.meta.auth) {
    router.push("/");
  }
};
</script>
