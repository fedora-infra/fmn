// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { defineStore } from "pinia";

export interface Toast {
  id: number;
  title?: string;
  content: string;
  color?: string;
  date: Date;
}

export const useToastStore = defineStore({
  id: "toast",
  state: () => ({
    toasts: [] as Toast[],
  }),
  actions: {
    addToast(toast: Omit<Toast, "id" | "date">) {
      this.toasts.push({
        ...toast,
        id: this.toasts.length,
        date: new Date(),
      });
    },
  },
});
