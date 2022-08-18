import type { TokenResponse } from "@openid/appauth";
import { defineStore } from "pinia";
import { useRoute } from "vue-router";
import { login, useAuth } from "../auth";
import type { UserInfoResponseJson } from "../auth/userinfo_request";

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
  }),
  getters: {
    user: (state) => ({ username: state.username, fullName: state.fullName }),
    loggedIn: (state) => !!(state.accessToken && state.username),
  },
  actions: {
    importTokenResponse(response: TokenResponse) {
      console.log("Got response:", response);
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
      console.log("User Info:", response);
      this.username = response.nickname || response.sub;
      this.fullName = response.name || this.username;
      this.email = response.email || "";
    },
    async getToken() {
      if (!this.accessToken) {
        return null;
      }
      const auth = useAuth();
      if (!auth) {
        return null;
      }
      if (this.tokenExpiresAt && Date.now() / 1000 > this.tokenExpiresAt) {
        // Refresh the token
        if (!this.refreshToken) {
          return null;
        }
        try {
          await auth.fetchServiceConfiguration();
          const result = await auth.makeAccessTokenRequest(this.refreshToken);
          this.importTokenResponse(result);
        } catch (err) {
          console.log("Could not refresh the access token:", err);
          this.logout();
          // TODO: redirect to the home page if we were on a protected page
          const currentRoute = useRoute();
          if (currentRoute.meta.auth) {
            console.log(
              "Logging in again, will redirect back to",
              currentRoute.fullPath,
              currentRoute
            );
            await login(auth, currentRoute.fullPath);
          }
        }
      }
      return this.accessToken;
    },
    logout() {
      this.$reset();
    },
  },
  persist: {
    storage: sessionStorage,
  },
});
