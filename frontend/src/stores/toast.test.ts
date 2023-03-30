// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { createPinia, setActivePinia } from "pinia";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { useToastStore } from "./toast";

describe("User Store", () => {
  beforeEach(() => {
    // creates a fresh pinia and make it active so it's automatically picked
    // up by any useStore() call without having to pass it to it:
    // `useStore(pinia)`
    setActivePinia(createPinia());
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });

  it("has no toast by default", () => {
    const store = useToastStore();
    expect(store.toasts.length).toBe(0);
  });

  it("can add a toast", () => {
    const store = useToastStore();
    const date = new Date(2000, 1, 1, 13);
    vi.setSystemTime(date);
    const msg = { title: "Title", content: "Content", color: "color" };
    store.addToast(msg);
    expect(store.toasts.length).toBe(1);
    expect(store.toasts[0]).toStrictEqual({
      ...msg,
      id: 0,
      date,
    });
  });
});
