import type { App } from "vue";
import { inject } from "vue";
import Authenticator from "./authenticator";

/* Fedora's open id connect provider */
const openIdConnectUrl = import.meta.env.VITE_OIDC_PROVIDER_URL;
/* client configuration */
const clientId = import.meta.env.VITE_OIDC_CLIENT_ID;
const redirectUri = new URL(
  `${import.meta.env.BASE_URL}login/fedora`,
  window.location.href
).href;
export const scope = "openid profile email";

export default (app: App) => {
  const auth = new Authenticator(openIdConnectUrl, clientId, redirectUri);
  app.config.globalProperties.$auth = auth;
  app.provide("auth", auth);
};

export function useAuth(): Authenticator | undefined {
  return inject("auth");
}
