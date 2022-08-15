import { createTestingPinia } from "@pinia/testing";
import { cleanup, fireEvent, render as baseRender } from "@testing-library/vue";
import { getActivePinia, setActivePinia, type Pinia } from "pinia";
import {
  afterEach,
  beforeEach,
  describe,
  expect,
  it,
  vi,
  type Mock,
} from "vitest";
import type { Component } from "vue";
import { createI18n } from "vue-i18n";
import * as auth from "../auth";
import router from "../router";
import { useUserStore } from "../stores/user";
import LoginButton from "./LoginButton.vue";

vi.mock("../auth");

const loginUser = (userStore: ReturnType<typeof useUserStore>) => {
  userStore.$patch({
    accessToken: "testing",
    username: "dummy-user",
    fullName: "Dummy User",
    email: "dummy@example.com",
  });
};

const render = (component: Component) => {
  const pinia = getActivePinia() as Pinia;
  const i18n = createI18n({
    legacy: false,
    locale: navigator.language,
    fallbackLocale: "en-US",
    messages: {},
  });
  return baseRender(component, {
    global: {
      plugins: [router, pinia, i18n],
      provide: {
        auth: vi.fn(),
      },
    },
  });
};

describe("LoginButton", () => {
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
    cleanup();
    vi.restoreAllMocks();
  });

  it("renders the login button when no user is logged in", () => {
    const userStore = useUserStore();
    expect(userStore.loggedIn).toBeFalsy();
    const { getByText } = render(LoginButton);
    getByText("Login");
  });

  it("renders the dropdown when a user is logged in", () => {
    const userStore = useUserStore();
    loginUser(userStore);

    const { getByText, getByAltText } = render(LoginButton);
    getByText("Logout");
    const elem = getByAltText<HTMLImageElement>("dummy-user");
    expect(elem.src).toBe(
      "https://www.libravatar.org/avatar/6e8e0bf6135471802a63a17c5e74ddc5?s=30&d=retro"
    );
  });

  it("logs the user out when logout is clicked", async () => {
    const userStore = useUserStore();
    loginUser(userStore);

    const routerSpy = vi.spyOn(router, "push");

    const { getByText } = render(LoginButton);
    await router.isReady();
    const logoutLink = getByText("Logout");
    await fireEvent.click(logoutLink);

    expect(auth.logout).toHaveBeenCalled();
    // No need to redirect
    expect(routerSpy).toHaveBeenCalledTimes(0);
  });

  it("redirects to the root page when logging out of a protected page", async () => {
    const userStore = useUserStore();
    loginUser(userStore);

    const rulesRoute = router.getRoutes().filter((r) => r.name === "rules")[0];
    const routerSpy = vi.spyOn(router, "push");

    const { getByText } = render(LoginButton);
    await router.isReady();
    await router.replace(rulesRoute.path);

    const logoutLink = getByText("Logout");
    await fireEvent.click(logoutLink);
    // We were on a protected page, we must redirect away.
    expect(routerSpy).toHaveBeenCalledOnce();
    expect(routerSpy).toHaveBeenCalledWith("/");
  });

  it("logs the user in when the login button is clicked", async () => {
    (auth.login as Mock).mockResolvedValue(null);
    (auth.useAuth as Mock).mockReturnValue("dummyAuthInstance");

    const { getByText } = render(LoginButton);
    await router.isReady();
    const loginLink = getByText("Login");
    await fireEvent.click(loginLink);

    expect(auth.login).toHaveBeenCalledOnce();
    expect(auth.login).toHaveBeenCalledWith("dummyAuthInstance", "/");
  });
});
