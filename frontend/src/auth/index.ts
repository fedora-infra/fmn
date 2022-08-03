import { useUserStore } from "@/stores/user";
import type { AppAuthError } from "@openid/appauth";
import type { App } from "vue";
import { inject } from "vue";
import type { Router } from "vue-router";
import Authenticator from "./authenticator";
import FedoraAuth from "./fedora";

export const login = async (
  auth: Authenticator | undefined,
  redirectTo: string,
  scopes: string[] = FedoraAuth.defaultScopes
) => {
  if (!auth) {
    throw new Error("The authentication is not ready, please try again later.");
  }

  // Store where we clicked the button
  localStorage.setItem("redirect_to", redirectTo);

  // Get the URLs from Ipsilon
  try {
    await auth.fetchServiceConfiguration();
  } catch (err) {
    console.log(err);
    // TODO: Ewww. Use flash messages or snackbar
    alert("Could not connect to Ipsilon: " + (err as AppAuthError).message);
  }
  // Start the authentication dance
  await auth.makeAuthorizationRequest(scopes.join(" "));
};

type Args = { router: Router };

export default (app: App, { router }: Args) => {
  const redirectUri = new URL(
    `${import.meta.env.BASE_URL}login/${FedoraAuth.name}`,
    window.location.href
  ).href;
  const auth = new Authenticator(
    FedoraAuth.openIdConnectUrl,
    FedoraAuth.clientId,
    redirectUri
  );
  app.config.globalProperties.$auth = auth;
  app.provide("auth", auth);

  router.beforeEach(async (to, from) => {
    const userStore = useUserStore();
    if (to.meta.auth && !userStore.loggedIn) {
      await login(auth, to.fullPath);
    }
  });
};

export function useAuth(): Authenticator | undefined {
  return inject("auth");
}
