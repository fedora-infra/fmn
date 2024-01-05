// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { useToastStore } from "@/stores/toast";
import { createTestingPinia } from "@pinia/testing";
import { setActivePinia } from "pinia";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import router from "../router";
import { useUserStore } from "../stores/user";
import type Authenticator from "./authenticator";
import { login, logout, useAuth } from "./index";

vi.mock("window.scrollTo");

const loginUser = (userStore: ReturnType<typeof useUserStore>) => {
  userStore.$patch({
    accessToken: "testing",
    username: "dummy-user",
    fullName: "Dummy User",
    email: "dummy@example.com",
  });
};

describe("auth", () => {
  beforeEach(async () => {
    await router.replace("/");
    // creates a fresh pinia and make it active so it's automatically picked
    // up by any useStore() call without having to pass it to it:
    // `useStore(pinia)`
    setActivePinia(
      createTestingPinia({
        createSpy: vi.fn,
        stubActions: false,
      }),
    );
  });
  // Unmount components after tests
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("logs the user out when logout is called", async () => {
    const userStore = useUserStore();
    loginUser(userStore);

    logout();

    expect(userStore.username).toBeNull();
    expect(userStore.fullName).toBeNull();
    expect(userStore.accessToken).toBeNull();
    expect(userStore.email).toBeNull();
    expect(userStore.loggedIn).toBeFalsy();
  });

  it("logs the user in when login is called", async () => {
    const authMock = {
      fetchServiceConfiguration: vi.fn().mockReturnValue(null),
      makeAuthorizationRequest: vi.fn().mockResolvedValue(null),
    } as unknown as Authenticator;

    await login(authMock, "/");

    expect(authMock.makeAuthorizationRequest).toHaveBeenCalledOnce();
    expect(authMock.makeAuthorizationRequest).toHaveBeenCalledWith(
      "openid profile email https://id.fedoraproject.org/scope/groups",
    );
    expect(sessionStorage.getItem("redirect_to")).toBe("/");
  });

  it("throws if authentication is not ready when login is called", async () => {
    await expect(login(undefined, "/")).rejects.toThrowError(
      "The authentication is not ready, please try again later.",
    );
  });

  it("throws and shows an error if provider is unavailable", async () => {
    const authMock = {
      fetchServiceConfiguration: vi
        .fn()
        .mockRejectedValue(new Error("dummy error")),
    } as unknown as Authenticator;
    const toastStore = useToastStore();

    await expect(login(authMock, "/")).rejects.toThrowError("dummy error");

    expect(toastStore.$state.toasts).toHaveLength(1);
    const toast = toastStore.$state.toasts[0];
    expect(toast.title).toBe("Authentication is impossible");
    expect(toast.content).toBe("Could not connect to Ipsilon: dummy error");
    expect(toast.color).toBe("danger");
  });

  it("throws if authentication is not ready when useAuth is called", async () => {
    expect(() => useAuth()).toThrowError("Authenticator is not ready");
  });
});
