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

export const apiGet: QueryFunction = async ({ queryKey }) => {
  const userStore = useUserStore(pinia);
  const token = await userStore.getToken();
  const url = queryKey[0] as string;
  const axiosConfig: AxiosRequestConfig = { params: queryKey[1] };
  if (token) {
    axiosConfig["headers"] = { Authorization: `Bearer ${token}` };
  }
  const response = await http.get(url, axiosConfig);
  return response.data;
};
