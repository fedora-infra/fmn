import { createTestingPinia } from "@pinia/testing";
import { setActivePinia } from "pinia";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import router from "../router";
import { useUserStore } from "../stores/user";
import type Authenticator from "./authenticator";
import { login, logout } from "./index";

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
      })
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
      "openid profile email https://id.fedoraproject.org/scope/groups"
    );
    expect(sessionStorage.getItem("redirect_to")).toBe("/");
  });
});
