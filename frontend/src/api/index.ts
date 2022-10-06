import { useUserStore } from "@/stores/user";
import axios, { type AxiosRequestConfig } from "axios";
import type { QueryFunction } from "react-query/types/core";
import type { VueQueryPluginOptions } from "vue-query";
import pinia from "../stores";

export const vueQueryPluginOptions: VueQueryPluginOptions = {
  queryClientConfig: {
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false,
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

export const apiGet: QueryFunction = async ({ queryKey }) => {
  const axiosConfig = await getAxiosConfig();
  const url = queryKey[0] as string;
  axiosConfig["params"] = queryKey[1];
  const response = await http.get(url, axiosConfig);
  return response.data;
};

export const apiPost = async (url: string, data: unknown) => {
  const axiosConfig = await getAxiosConfig();
  const response = await http.post(url, data, axiosConfig);
  return response.data;
};

export const apiPut = async (url: string, data: unknown) => {
  const axiosConfig = await getAxiosConfig();
  const response = await http.put(url, data, axiosConfig);
  return response.data;
};

export const apiDelete = async (url: string) => {
  const axiosConfig = await getAxiosConfig();
  const response = await http.delete(url, axiosConfig);
  return response.data;
};
