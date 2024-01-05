// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import {
  AuthorizationRequest,
  AuthorizationResponse,
  FetchRequestor,
} from "@openid/appauth";
import { waitFor } from "@testing-library/vue";
import {
  afterEach,
  beforeEach,
  describe,
  expect,
  it,
  vi,
  type MockedObject,
} from "vitest";
import Authenticator from "./authenticator";

const PROVIDER_URL = "https://id.example.test";
const CLIENT_ID = "dummy-client-id";
const REDIRECT_URL = "/oidc-callback";
const OPENID_CONFIGURATION = {
  authorization_endpoint: PROVIDER_URL + "/auth",
  token_endpoint: PROVIDER_URL + "/token",
  userinfo_endpoint: PROVIDER_URL + "/userinfo",
  revocation_endpoint: PROVIDER_URL + "/revoke",
};
const REFRESH_TOKEN = {
  access_token: "dummy-access-token",
  refresh_token: "dummy-refresh-token",
  scope: "dummy-serverside-scope",
  id_token: "dummy-id-token",
};
const USER_INFO = {
  sub: "dummy-sub",
  name: "dummy-name",
  nickname: "dummy-nickname",
  email: "dummy-email",
};

vi.mock("@openid/appauth", async (importOriginal) => {
  const FetchRequestor = vi.fn();
  FetchRequestor.prototype.xhr = vi.fn();
  const mod = await importOriginal();
  return {
    ...(mod as object),
    FetchRequestor,
  };
});
vi.stubGlobal("location", {
  assign: vi.fn(),
});

const getStateFromStorage = async (): Promise<string> => {
  let key = "appauth_current_authorization_request";
  await waitFor(() => {
    expect(window.localStorage.getItem(key)).not.toBeNull();
  });
  const sess = window.localStorage.getItem(key);
  key = `${sess}_appauth_authorization_request`;
  await waitFor(() => {
    expect(window.localStorage.getItem(key)).not.toBeNull();
  });
  const sessDetails = window.localStorage.getItem(key);
  return JSON.parse(sessDetails as string).state;
};

describe("authenticator", () => {
  let requestor: MockedObject<FetchRequestor>;
  let auth: Authenticator;

  beforeEach(async () => {
    auth = new Authenticator(PROVIDER_URL, CLIENT_ID, REDIRECT_URL);
    // Mock HTTP requests
    requestor = vi.mocked(new FetchRequestor());
    requestor.xhr.mockImplementation(async ({ url }) => {
      if (url === PROVIDER_URL + "/.well-known/openid-configuration") {
        return OPENID_CONFIGURATION;
      } else if (url === PROVIDER_URL + "/token") {
        return REFRESH_TOKEN;
      } else if (url === PROVIDER_URL + "/userinfo") {
        return USER_INFO;
      } else if (url === PROVIDER_URL + "/revoke") {
        return "";
      }
      throw new Error(`Unmocked URL: ${url}`);
    });
  });
  // Unmount components after tests
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("fetches service configuration", async () => {
    const result = await auth.fetchServiceConfiguration();
    expect(requestor.xhr).toHaveBeenCalledWith({
      url: "https://id.example.test/.well-known/openid-configuration",
      dataType: "json",
      method: "GET",
    });
    expect(result.tokenEndpoint).toBe(PROVIDER_URL + "/token");
    expect(result.authorizationEndpoint).toBe(PROVIDER_URL + "/auth");
  });

  it("caches service configuration", async () => {
    await auth.fetchServiceConfiguration();
    // This one should hit the cache.
    await auth.fetchServiceConfiguration();
    expect(requestor.xhr).toHaveBeenCalledOnce();
  });

  it("makes authorization requests", async () => {
    await auth.fetchServiceConfiguration();
    auth.makeAuthorizationRequest("dummy-scope");
    // The redirect is done async
    await waitFor(() => {
      expect(window.location.assign).toHaveBeenCalledOnce();
    });
    const state = await getStateFromStorage();
    // Now check the redirect
    const expected = `https://id.example.test/auth?redirect_uri=%2Foidc-callback&client_id=dummy-client-id&response_type=code&state=${state}&scope=dummy-scope`;
    // We can't use toHaveBeenCalledWith() because depending on the platform's features the
    // appauth library will or will not use PKCE and thus add a random code_challenge to the
    // query string.
    // expect(window.location.assign).toHaveBeenCalledWith(expected);
    expect(window.location.assign).toHaveBeenCalledTimes(1);
    const redirectCall = vi.mocked(window.location.assign).mock.lastCall;
    expect(redirectCall).toBeDefined();
    expect(redirectCall).toHaveLength(1);
    expect(redirectCall![0]).toContain(expected);
  });

  it("throws on authorization requests without config", async () => {
    expect(() => auth.makeAuthorizationRequest("dummy-scope")).toThrowError(
      "Configuration is not initialized",
    );
  });

  it("handles authorization redirects", async () => {
    await auth.fetchServiceConfiguration();
    auth.makeAuthorizationRequest("dummy-scope");
    const state = await getStateFromStorage();
    window.location.search = `state=${state}&code=dummy-code`;

    const result = await auth.handleAuthorizationRedirect();

    expect(result.accessToken).toBe(REFRESH_TOKEN.access_token);
    expect(result.refreshToken).toBe(REFRESH_TOKEN.refresh_token);
    expect(result.scope).toBe(REFRESH_TOKEN.scope);
  });

  it("show error when authorization response is a failure", async () => {
    await auth.fetchServiceConfiguration();
    auth.makeAuthorizationRequest("dummy-scope");
    const state = await getStateFromStorage();
    window.location.search = `state=${state}&error=dummy-error&error_description=dummy-error-desc`;

    expect(auth.handleAuthorizationRedirect()).rejects.toThrow(
      "dummy-error-desc",
    );
  });

  it("show error when authorization response is incomplete", async () => {
    await auth.fetchServiceConfiguration();
    auth.makeAuthorizationRequest("dummy-scope");
    const state = await getStateFromStorage();
    window.location.search = `state=${state}&code=dummy-code`;
    requestor.xhr.mockImplementation(async () => ({ foo: "bar" }));

    expect(auth.handleAuthorizationRedirect()).rejects.toThrow(
      "No refresh_token in response",
    );
  });

  it("makes access token requests", async () => {
    await auth.fetchServiceConfiguration();

    const response = await auth.makeAccessTokenRequest("dummy-refresh-token");

    expect(requestor.xhr).toHaveBeenCalledWith({
      url: "https://id.example.test/token",
      dataType: "json",
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      data: "grant_type=refresh_token&client_id=dummy-client-id&redirect_uri=%2Foidc-callback&refresh_token=dummy-refresh-token",
    });
    expect(response.accessToken).toBe(REFRESH_TOKEN.access_token);
    expect(response.refreshToken).toBe(REFRESH_TOKEN.refresh_token);
    expect(response.scope).toBe(REFRESH_TOKEN.scope);
  });

  it("throws on access token requests without config", async () => {
    expect(() =>
      auth.makeAccessTokenRequest("dummy-refresh-token"),
    ).toThrowError("Configuration is not initialized");
  });

  it("throws on refresh token requests without config", async () => {
    expect(() =>
      auth.makeRefreshTokenRequest(
        new AuthorizationRequest({
          response_type: "",
          client_id: "",
          redirect_uri: "",
          scope: "",
        }),
        new AuthorizationResponse({ code: "", state: "" }),
      ),
    ).toThrowError("Configuration is not initialized");
  });

  it("throws on malformed access token responses", async () => {
    await auth.fetchServiceConfiguration();
    requestor.xhr.mockImplementation(async () => ({ foo: "bar" }));

    await expect(
      auth.makeAccessTokenRequest("dummy-refresh-token"),
    ).rejects.toThrowError("No access_token in response");
  });

  it("makes userinfo requests", async () => {
    await auth.fetchServiceConfiguration();

    const response = await auth.makeUserInfoRequest("dummy-access-token");

    expect(requestor.xhr).toHaveBeenCalledWith({
      url: "https://id.example.test/userinfo",
      dataType: "json",
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      data: "access_token=dummy-access-token",
    });
    expect(response).toBe(USER_INFO);
  });

  it("makes userinfo requests without config", async () => {
    expect(() => auth.makeUserInfoRequest("dummy-access-token")).toThrowError(
      "Configuration is not initialized",
    );
  });

  it("makes token revocation requests", async () => {
    await auth.fetchServiceConfiguration();

    const response = await auth.makeRevokeTokenRequest("dummy-token");

    expect(requestor.xhr).toHaveBeenCalledWith({
      url: "https://id.example.test/revoke",
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      data: "token=dummy-token",
    });
    expect(response).toBe(true);
  });

  it("throws on revocation requests without config", async () => {
    expect(() => auth.makeRevokeTokenRequest("dummy-token")).toThrowError(
      "Configuration is not initialized",
    );
  });
});

/* Dump localStorage
const keys = Object.keys(window.localStorage);
for (const key of keys) {
  console.log(`${key}: ${window.localStorage.getItem(key)}`);
}
*/
