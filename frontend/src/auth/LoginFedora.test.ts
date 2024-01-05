// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { apiClient } from "@/api/__mocks__";
import { useToastStore } from "@/stores/toast";
import { useUserStore } from "@/stores/user";
import { getRenderOptions } from "@/util/tests";
import { TokenResponse } from "@openid/appauth";
import {
  cleanup,
  render,
  screen,
  waitFor,
  type RenderOptions,
} from "@testing-library/vue";
import { AxiosError, AxiosHeaders, type AxiosResponse } from "axios";
import { createPinia, setActivePinia } from "pinia";
import {
  afterEach,
  beforeEach,
  describe,
  expect,
  it,
  vi,
  type Mocked,
} from "vitest";
import router from "../router";
import LoginFedora from "./LoginFedora.vue";
import type Authenticator from "./authenticator";

vi.mock("window.scrollTo");
vi.mock("@/api");

describe("LoginFedora", () => {
  let tokenResponse: TokenResponse;
  let renderOptions: RenderOptions;
  let auth: Mocked<Authenticator>;

  beforeEach(async () => {
    await router.replace("/login/fedora");
    await router.isReady();
    setActivePinia(createPinia());
    renderOptions = getRenderOptions();
    auth = renderOptions.global?.provide?.auth;
    auth.handleAuthorizationRedirect.mockImplementation(
      async () => tokenResponse,
    );
  });
  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
    sessionStorage.clear();
  });

  it("renders", () => {
    const { getByText } = render(LoginFedora, renderOptions);
    expect(getByText("Loading user information...")).toBeInTheDocument();
  });

  it("redirects if already logged in", async () => {
    const store = useUserStore();
    store.$patch({
      accessToken: "testing",
      username: "dummy-user",
      fullName: "Dummy User",
      email: "dummy@example.com",
    });
    render(LoginFedora, renderOptions);
    await waitFor(() => {
      expect(router.currentRoute.value.path).toBe("/");
    });
  });

  it("handles the incoming OIDC data", async () => {
    tokenResponse = new TokenResponse({
      access_token: "dummy-access-token",
      refresh_token: "dummy-refresh-token",
      scope: "dummy-serverside-scope",
    });
    const userInfoResponse = {
      sub: "dummy-sub",
      nickname: "dummy-username",
    };
    auth.makeUserInfoRequest.mockResolvedValue(userInfoResponse);
    vi.mocked(apiClient.get).mockResolvedValue({ data: { is_admin: false } });

    render(LoginFedora, renderOptions);

    const store = useUserStore();

    await waitFor(() => {
      expect(store.loggedIn).toBe(true);
      // The call to the API is async
      expect(vi.mocked(apiClient.get)).toHaveBeenCalled();
    });

    expect(auth.makeUserInfoRequest).toHaveBeenCalledWith("dummy-access-token");
    expect(vi.mocked(apiClient.get)).toHaveBeenCalledWith("/api/v1/users/me");
    expect(store.$state).toStrictEqual({
      accessToken: "dummy-access-token",
      refreshToken: "dummy-refresh-token",
      idToken: null,
      tokenExpiresAt: null,
      scopes: [],
      username: "dummy-username",
      fullName: "dummy-username",
      email: "",
      isAdmin: false,
    });
    // We must have been redirected
    await waitFor(() => {
      expect(router.currentRoute.value.path).toBe("/");
    });
    const toastStore = useToastStore();
    expect(toastStore.toasts).toHaveLength(1);
    expect(toastStore.toasts[0].title).toBe("Login successful!");
    expect(toastStore.toasts[0].content).toBe("Welcome, dummy-username.");
    expect(toastStore.toasts[0].color).toBe("success");
  });

  it("handles the incoming OIDC data about an admin", async () => {
    tokenResponse = new TokenResponse({
      access_token: "dummy-access-token",
      refresh_token: "dummy-refresh-token",
      scope: "dummy-serverside-scope",
    });
    auth.makeUserInfoRequest.mockResolvedValue({
      sub: "dummy-sub",
      nickname: "dummy-username",
    });
    vi.mocked(apiClient.get).mockResolvedValue({ data: { is_admin: true } });

    render(LoginFedora, renderOptions);

    const store = useUserStore();

    await waitFor(() => {
      expect(vi.mocked(apiClient.get)).toHaveBeenCalled();
    });
    expect(store.loggedIn).toBe(true);
    expect(store.isAdmin).toBe(true);
  });

  it("displays authentication errors", async () => {
    const { getByText } = render(LoginFedora, renderOptions);
    auth.handleAuthorizationRedirect.mockRejectedValue("Dummy Error");
    await waitFor(() => {
      expect(getByText("Dummy Error")).toBeInTheDocument();
    });
  });

  it("handles API errors when getting user info", async () => {
    tokenResponse = new TokenResponse({
      access_token: "dummy-access-token",
    });
    auth.makeUserInfoRequest.mockResolvedValue({
      sub: "dummy-sub",
      nickname: "dummy-username",
    });

    const mockedErrorResponse: AxiosResponse = {
      status: 500,
      statusText: "Server Error",
      headers: AxiosHeaders.from(""),
      config: { headers: AxiosHeaders.from("") },
      data: { detail: "dummy API error" },
    };
    vi.mocked(apiClient.get).mockRejectedValue(
      new AxiosError<{ detail: string }>(
        "dummy error",
        "500",
        undefined,
        undefined,
        mockedErrorResponse,
      ),
    );

    render(LoginFedora, renderOptions);

    const store = useUserStore();

    await waitFor(() => {
      // The call to the API is async
      expect(vi.mocked(apiClient.get)).toHaveBeenCalled();
    });

    // We must be logged out
    expect(store.$state).toStrictEqual({
      accessToken: null,
      refreshToken: null,
      idToken: null,
      tokenExpiresAt: null,
      scopes: [],
      username: null,
      fullName: null,
      email: null,
      isAdmin: false,
    });
    // We must not have been redirected
    expect(router.currentRoute.value.path).toBe("/login/fedora");
    // There should be a "login failed" alert.
    screen.getByText("Login failed!");
    screen.getByText(
      "Could not retrieve user information from the API: dummy API error.",
    );
  });

  it("redirects to the right place on login", async () => {
    tokenResponse = new TokenResponse({
      access_token: "dummy-access-token",
    });
    auth.makeUserInfoRequest.mockResolvedValue({
      sub: "dummy-sub",
      nickname: "dummy-username",
    });
    vi.mocked(apiClient.get).mockResolvedValue({ data: { is_admin: false } });
    sessionStorage.setItem("redirect_to", "/dummy/page");

    render(LoginFedora, renderOptions);

    await waitFor(() => {
      expect(router.currentRoute.value.path).toBe("/dummy/page");
    });
    expect(sessionStorage.getItem("redirect_to")).toBeNull();
  });

  it("displays authentication errors", async () => {
    const { getByText } = render(LoginFedora, renderOptions);
    auth.handleAuthorizationRedirect.mockRejectedValue("Dummy Error");
    await waitFor(() => {
      expect(getByText("Dummy Error")).toBeInTheDocument();
    });
  });
});
