// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { useUserStore } from "@/stores/user";
import type { QueryFunctionContext } from "@tanstack/query-core";
import type { VueQueryPluginOptions } from "@tanstack/vue-query";
import axios, { type AxiosRequestConfig } from "axios";
import pinia from "../stores";
import type { APIError, HTTPValidationError, Nullable } from "./types";

export const vueQueryPluginOptions: VueQueryPluginOptions = {
  queryClientConfig: {
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false,
        retry: (failureCount, error) => {
          const errorResponse = (error as APIError).response;
          if (errorResponse && errorResponse.status < 500) {
            return false; // Don't retry for client-side errors, it won't help.
          }
          return failureCount <= 3;
        },
      },
    },
  },
};

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

async function getAxiosConfig() {
  const userStore = useUserStore(pinia);
  const token = await userStore.getToken();
  const axiosConfig: AxiosRequestConfig = {
    // Don't add brackets to arrays
    // paramsSerializer: (params) => stringify(params, { arrayFormat: "repeat" }),
    // For Axios 1.0+
    paramsSerializer: { indexes: null },
  };
  if (token) {
    axiosConfig["headers"] = { Authorization: `Bearer ${token}` };
  }
  return axiosConfig;
}

export async function getApiClient() {
  const axiosConfig = await getAxiosConfig();
  return axios.create({
    ...http.defaults,
    ...axiosConfig,
  });
}

interface QueryFunctionContextOrDirect
  extends Omit<QueryFunctionContext, "signal" | "meta"> {
  signal?: QueryFunctionContext["signal"];
  meta?: QueryFunctionContext["meta"];
}
export const apiGet = async <Data>({
  queryKey,
  signal,
}: QueryFunctionContextOrDirect) => {
  const axiosConfig = await getAxiosConfig();
  const url = queryKey[0] as string;
  axiosConfig["params"] = queryKey[1];
  axiosConfig["signal"] = signal;
  const response = await http.get<Data>(url, axiosConfig);
  return response.data;
};

export const apiPost = async <Data, InputData = Partial<Data>>(
  url: string,
  data: InputData,
) => {
  const axiosConfig = await getAxiosConfig();
  const response = await http.post<Data>(url, data, axiosConfig);
  return response.data;
};

export const apiPut = async <Data>(url: string, data: Data) => {
  const axiosConfig = await getAxiosConfig();
  const response = await http.put<Data>(url, data, axiosConfig);
  return response.data;
};

export const apiDelete = async <Data>(url: string) => {
  const axiosConfig = await getAxiosConfig();
  const response = await http.delete<Data>(url, axiosConfig);
  return response.data;
};

export const apiPatch = async <Data, InputData = Nullable<Partial<Data>>>(
  url: string,
  data: InputData,
) => {
  const axiosConfig = await getAxiosConfig();
  const response = await http.patch<Data>(url, data, axiosConfig);
  return response.data;
};

export const validationErrorToFormErrors = (data: HTTPValidationError) => {
  const detail = data.detail || [];
  if (Array.isArray(detail)) {
    return detail.map((e) => `Server error: ${e.loc[-1]}: ${e.msg}`);
  } else {
    return [detail];
  }
};
