import { useUserStore } from "@/stores/user";
import type { QueryFunction } from "react-query/types/core";
import { useMutation, useQuery, useQueryClient } from "vue-query";
import { apiDelete, apiGet, apiPatch, apiPost, apiPut } from "./index";
import type {
  NewRule,
  PostError,
  PreviewNotification,
  Rule,
  RulePatch,
} from "./types";

// Get all rules
export const useRulesQuery = () => {
  const userStore = useUserStore();
  const url = `/api/v1/users/${userStore.username}/rules`;
  return useQuery(url, apiGet as QueryFunction<Rule[]>, {
    enabled: userStore.loggedIn,
  });
};

// Add a new rule
export const useAddRuleMutation = () => {
  const userStore = useUserStore();
  const client = useQueryClient();

  return useMutation<Rule, PostError, NewRule>(
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
  return useMutation<Rule, PostError, Rule>((data) => apiPut(url, data), {
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
  return useMutation<void, PostError, number>(
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
export const usePreviewRuleQuery = (data: NewRule) => {
  const doApiPost: QueryFunction<PreviewNotification[]> = () =>
    apiPost(url, data);
  const url = "/api/v1/rule-preview";
  console.log("Previewing rule:", data);
  return useQuery([url, data], doApiPost, { retry: false });
};

// Get disabled rules
export const useDisabledRulesQuery = () => {
  const url = "/api/v1/admin/rules";
  return useQuery([url, { disabled: true }], apiGet as QueryFunction<Rule[]>);
};

// Patch an existing rule
export const usePatchRuleMutation = () => {
  const client = useQueryClient();
  return useMutation<Rule, PostError, { id: Rule["id"]; rule: RulePatch }>(
    ({ id, rule }) => {
      return apiPatch(`/api/v1/admin/rules/${id}`, rule);
    },
    {
      onSuccess: async () => {
        await client.invalidateQueries([
          "/api/v1/admin/rules",
          {
            disabled: true,
          },
        ]);
      },
    }
  );
};
