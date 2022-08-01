import axios from "axios";
import type { QueryFunction } from "react-query/types/core";

export const apiGet: QueryFunction = async ({ queryKey }) => {
  const url = import.meta.env.VITE_API_URL + queryKey[0];
  const axiosConfig = { params: queryKey[1] };
  const response = await axios.get(url, axiosConfig);
  console.log(response);
  return response.data;
};
