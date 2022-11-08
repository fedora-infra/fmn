import { useUserStore } from "@/stores/user";
import type { QueryFunction } from "react-query/types/core";
import { useMutation, useQuery, useQueryClient } from "vue-query";
import { apiDelete, apiGet, apiPost, apiPut } from "./index";
import type { Notification, Rule } from "./types";

// Get all rules
export const useRulesQuery = () => {
  const userStore = useUserStore();
  const url = `/api/v1/users/${userStore.username}/rules`;
  return useQuery(url, apiGet as QueryFunction<Rule[]>);
};

// Add a new rule
export const useAddRuleMutation = () => {
  const userStore = useUserStore();
  const client = useQueryClient();

  return useMutation<Rule, unknown, Rule>(
    (data) => apiPost(`/api/v1/users/${userStore.username}/rules`, data),
    {
      onSuccess: async () => {
        await client.invalidateQueries([
          `/api/v1/users/${userStore.username}/rules`,
        ]);
      },
    }
  );
};

// Edit a rule
export const useEditRuleMutation = (id: number) => {
  const userStore = useUserStore();
  const client = useQueryClient();
  const url = `/api/v1/users/${userStore.username}/rules/${id}`;
  return useMutation<Rule, unknown, Rule>((data) => apiPut(url, data), {
    onSuccess: async () => {
      await client.invalidateQueries([url]);
      await client.invalidateQueries([
        `/api/v1/users/${userStore.username}/rules`,
      ]);
    },
  });
};

// Add a new rule
export const useDeleteRuleMutation = () => {
  const userStore = useUserStore();
  const client = useQueryClient();
  return useMutation<void, unknown, number>(
    (id) => apiDelete(`/api/v1/users/${userStore.username}/rules/${id}`),
    {
      onSuccess: async () => {
        const url = `/api/v1/users/${userStore.username}/rules`;
        await client.invalidateQueries(url, { refetchActive: true });
      },
    }
  );
};

// Preview a rule
export const usePreviewRuleQuery = (data: Omit<Rule, "id">) => {
  const doApiPost: QueryFunction<Notification[]> = () => apiPost(url, data);
  const url = "/api/v1/rule-preview";
  console.log("Previewing rule:", data);
  return useQuery([url, data], doApiPost, { retry: false });
};
