<template>
  <CDropdown v-if="userStore.loggedIn" variant="nav-item" alignment="end">
    <CDropdownToggle component="a">
      <img :alt="userStore.user.username!" :src="avatarURL" />
    </CDropdownToggle>
    <CDropdownMenu>
      <CDropdownItem @click="doLogout()">Logout</CDropdownItem>
    </CDropdownMenu>
  </CDropdown>
  <CNavItem v-else>
    <CButton @click.prevent="doLogin()" component="a" color="primary">
      Login
    </CButton>
  </CNavItem>
</template>

<script setup lang="ts">
import {
  CButton,
  CDropdown,
  CDropdownToggle,
  CDropdownMenu,
  CDropdownItem,
  CNavItem,
} from "@coreui/bootstrap-vue";
import { useRoute, useRouter } from "vue-router";
import { login, logout, useAuth } from "../auth";
import { useUserStore } from "../stores/user";
import { generateLibravatarURL } from "../util";

const auth = useAuth();
const route = useRoute();
const userStore = useUserStore();
const router = useRouter();
const avatarURL = generateLibravatarURL(userStore.email, 30, "retro");

const doLogin = () => login(auth, route.fullPath);

const doLogout = () => {
  logout();
  if (route.meta.auth) {
    router.push("/");
  }
};
</script>
