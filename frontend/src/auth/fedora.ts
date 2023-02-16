/* Fedora's open id connect provider */
const FedoraAuth = {
  name: "fedora",
  openIdConnectUrl: import.meta.env.VITE_OIDC_PROVIDER_URL,
  clientId: import.meta.env.VITE_OIDC_CLIENT_ID,
  defaultScopes: [
    "openid",
    "profile",
    "email",
    "https://id.fedoraproject.org/scope/groups",
  ],
};

export default FedoraAuth;
