// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { createTestingPinia } from "@pinia/testing";
import { cleanup } from "@testing-library/vue";
import { setActivePinia } from "pinia";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import router from "../router";
import { useUserStore } from "../stores/user";
import AdminLink from "./AdminLink.vue";
import { loginAdmin, loginUser, render } from "./test-utils";

vi.mock("window.scrollTo");
vi.mock("../auth");

describe("AdminLink", () => {
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
    cleanup();
    vi.restoreAllMocks();
  });

  it("doesnt render the admin link when not logged in", () => {
    const userStore = useUserStore();
    expect(userStore.loggedIn).toBeFalsy();
    const { queryAllByText } = render(AdminLink);
    expect(queryAllByText("Admin")).toStrictEqual([]);
  });

  it("doesnt render the admin link when logged in as non-admin", () => {
    const userStore = useUserStore();
    loginUser(userStore);
    const { queryAllByText } = render(AdminLink);
    expect(queryAllByText("Admin")).toStrictEqual([]);
  });

  it("renders the admin link when not logged in as an admin", () => {
    const userStore = useUserStore();
    loginAdmin(userStore);
    const { getByText } = render(AdminLink);
    expect(getByText("Admin")).toBeInTheDocument();
  });
});
