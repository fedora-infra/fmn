// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import axios, { type AxiosInstance } from "axios";
import { vi } from "vitest";

export const apiClient = {
  defaults: axios.defaults,
  get: vi.fn(),
} as unknown as AxiosInstance;

export async function getApiClient() {
  return apiClient;
}
