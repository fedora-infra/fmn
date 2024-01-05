// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import type Authenticator from "@/auth/authenticator";
import { TokenResponse } from "@openid/appauth";
import { createPinia, setActivePinia } from "pinia";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import router from "../router";
import { useUserStore } from "./user";

vi.mock("window.scrollTo");

describe("User Store", () => {
  beforeEach(async () => {
    await router.replace("/");
    // creates a fresh pinia and make it active so it's automatically picked
    // up by any useStore() call without having to pass it to it:
    // `useStore(pinia)`
    setActivePinia(createPinia());
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("is logged out by default", () => {
    const store = useUserStore();
    expect(store.loggedIn).toBeFalsy();
    expect(store.username).toBe(null);
    expect(store.user).toStrictEqual({ username: null, fullName: null });
  });

  it("imports token responses", () => {
    const store = useUserStore();
    const tokenResponse = new TokenResponse({
      access_token: "access-token",
      refresh_token: "refresh-token",
      id_token: "id-token",
      issued_at: 42,
      expires_in: "8",
    });
    store.importTokenResponse(tokenResponse);
    expect(store.loggedIn).toBeFalsy();
    expect(store.accessToken).toBe(tokenResponse.accessToken);
    expect(store.refreshToken).toBe(tokenResponse.refreshToken);
    expect(store.idToken).toBe(tokenResponse.idToken);
    expect(store.tokenExpiresAt).toBe(50);
  });

  it("imports user info responses", () => {
    const store = useUserStore();
    store.accessToken = "access-token";
    store.importUserInfoResponse({
      sub: "sub",
      nickname: "nickname",
      name: "Name",
      email: "user@example.com",
    });
    expect(store.loggedIn).toBeTruthy();
    expect(store.username).toBe("nickname");
    expect(store.fullName).toBe("Name");
    expect(store.email).toBe("user@example.com");
    // Only the minimum required information
    store.importUserInfoResponse({
      sub: "sub",
    });
    expect(store.username).toBe("sub");
    expect(store.fullName).toBe("sub");
    expect(store.email).toBe("");
  });

  it("resets on logout", () => {
    const store = useUserStore();
    store.$patch({
      accessToken: "testing",
      username: "dummy-user",
      fullName: "Dummy User",
      email: "dummy@example.com",
    });
    expect(store.loggedIn).toBeTruthy();
    store.logout();
    expect(store.loggedIn).toBeFalsy();
    expect(store.user).toStrictEqual({ username: null, fullName: null });
  });

  it("returns null when calling getToken with no access token", async () => {
    const store = useUserStore();
    expect(await store.getToken()).toBe(null);
  });

  it("refreshes access tokens", async () => {
    const store = useUserStore();
    store.$auth = vi.fn() as unknown as Authenticator;
    store.$auth.makeAccessTokenRequest = vi
      .fn()
      .mockResolvedValue({ accessToken: "new-access-token" });
    store.accessToken = "access-token";
    store.refreshToken = "refresh-token";
    store.tokenExpiresAt = 1;
    store.$auth.fetchServiceConfiguration = vi.fn().mockResolvedValue({});
    expect(await store.getToken()).toBe("new-access-token");
    expect(store.$auth.makeAccessTokenRequest).toHaveBeenCalledWith(
      "refresh-token",
    );
  });

  it("logs in again when refreshing with no refresh token", async () => {
    const store = useUserStore();
    store.accessToken = "access-token";
    store.tokenExpiresAt = 1;
    store.logoutAndLogin = vi.fn().mockImplementation(async () => {
      store.accessToken = "new-access-token";
    });
    expect(await store.getToken()).toBe("new-access-token");
    expect(store.logoutAndLogin).toHaveBeenCalledOnce();
  });

  it("logs in again when refreshing and refresh fails", async () => {
    const store = useUserStore();
    store.accessToken = "access-token";
    store.refreshToken = "refresh-token";
    store.tokenExpiresAt = 1;
    store.logoutAndLogin = vi.fn().mockImplementation(async () => {
      store.accessToken = "new-access-token";
    });
    store.$auth = vi.fn() as unknown as Authenticator;
    store.$auth.fetchServiceConfiguration = vi.fn().mockResolvedValue({});
    store.$auth.makeAccessTokenRequest = vi
      .fn()
      .mockRejectedValue("refresh failure");
    expect(await store.getToken()).toBe("new-access-token");
    expect(store.logoutAndLogin).toHaveBeenCalledOnce();
  });

  it("logs out and requests a login when logoutAndLogin is called", async () => {
    const store = useUserStore();
    store.$patch({
      accessToken: "testing",
      username: "dummy-user",
      fullName: "Dummy User",
      email: "dummy@example.com",
    });
    expect(store.loggedIn).toBeTruthy();

    store.$auth = vi.fn() as unknown as Authenticator;
    store.$auth.fetchServiceConfiguration = vi.fn().mockResolvedValue({});
    store.$auth.makeAuthorizationRequest = vi.fn().mockResolvedValue(null);

    store.$router = router;
    const newruleRoute = store.$router
      .getRoutes()
      .filter((r) => r.name === "new-rule")[0];
    await store.$router.isReady();
    await store.$router.replace(newruleRoute.path);

    await store.logoutAndLogin();
    expect(store.loggedIn).toBeFalsy();
    expect(store.$auth.makeAuthorizationRequest).toHaveBeenCalledWith(
      "openid profile email https://id.fedoraproject.org/scope/groups",
    );
  });
});
