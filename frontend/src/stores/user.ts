// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import type { TokenResponse } from "@openid/appauth";
import { defineStore } from "pinia";
import { isRef } from "vue";
import { login } from "../auth";
import type { UserInfoResponseJson } from "../auth/userinfo_request";
import { useToastStore } from "./toast";

export const useUserStore = defineStore({
  id: "user",
  state: () => ({
    accessToken: null as string | null,
    refreshToken: null as string | null,
    idToken: null as string | null,
    tokenExpiresAt: null as number | null,
    scopes: [],
    username: null as string | null,
    fullName: null as string | null,
    email: null as string | null,
    isAdmin: false,
  }),
  getters: {
    user: (state) => ({ username: state.username, fullName: state.fullName }),
    loggedIn: (state) => !!(state.accessToken && state.username),
  },
  actions: {
    importTokenResponse(response: TokenResponse) {
      console.log("Got OIDC token response:", response);
      if (response.accessToken) {
        this.accessToken = response.accessToken;
      }
      if (response.refreshToken) {
        this.refreshToken = response.refreshToken;
      }
      if (response.idToken) {
        this.idToken = response.idToken;
      }
      if (response.issuedAt && response.expiresIn) {
        this.tokenExpiresAt = response.issuedAt + response.expiresIn;
      }
    },
    importUserInfoResponse(response: UserInfoResponseJson) {
      console.log("Got user info response:", response);
      this.username = response.nickname || response.sub;
      this.fullName = response.name || this.username;
      this.email = response.email || "";
    },
    setAdmin(value: boolean) {
      this.isAdmin = value;
    },
    async getToken() {
      if (!this.accessToken) {
        return null;
      }
      const auth = this.$auth;
      if (this.tokenExpiresAt && Date.now() / 1000 > this.tokenExpiresAt) {
        // Refresh the token
        if (!this.refreshToken) {
          console.log("No refresh token, logging in again.");
          await this.logoutAndLogin();
          return this.accessToken;
        }
        try {
          await auth.fetchServiceConfiguration();
          const result = await auth.makeAccessTokenRequest(this.refreshToken);
          this.importTokenResponse(result);
        } catch (err) {
          const toastStore = useToastStore();
          console.log("Could not refresh the access token:", err);
          toastStore.addToast({
            title: "Session expired",
            content: "Your session has expired, please log in again",
            color: "warning",
          });
          await this.logoutAndLogin();
        }
      }
      return this.accessToken;
    },
    logout() {
      this.$reset();
    },
    async logoutAndLogin() {
      this.logout();
      const currentRoute = isRef(this.$router.currentRoute)
        ? this.$router.currentRoute.value
        : this.$router.currentRoute;
      if (currentRoute.meta.auth) {
        console.log(
          "Logging in again, will redirect back to",
          currentRoute.fullPath,
          currentRoute,
        );
        await login(this.$auth, currentRoute.fullPath);
      }
    },
  },
  persist: {
    storage: localStorage,
  },
});
