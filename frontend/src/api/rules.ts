// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { useUserStore } from "@/stores/user";
import { useMutation, useQuery, useQueryClient } from "vue-query";
import { apiDelete, apiGet, apiPatch, apiPost, apiPut } from "./index";
import type { NewRule, PostError, Rule, RulePatch } from "./types";

// Get all rules
export const useRulesQuery = () => {
  const userStore = useUserStore();
  const url = `/api/v1/users/${userStore.username}/rules`;
  return useQuery(url, apiGet<Rule[]>, {
    enabled: userStore.loggedIn,
  });
};

// Add a new rule
export const useAddRuleMutation = () => {
  const userStore = useUserStore();
  const client = useQueryClient();

  return useMutation<Rule, PostError, NewRule>(
    (data) => apiPost<Rule>(`/api/v1/users/${userStore.username}/rules`, data),
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

// Get disabled rules
export const useDisabledRulesQuery = () => {
  const url = "/api/v1/admin/rules";
  return useQuery<Rule[]>([url, { disabled: true }], apiGet);
};

// Patch an existing rule
export const usePatchRuleMutation = () => {
  const client = useQueryClient();
  return useMutation<Rule, PostError, { id: Rule["id"]; rule: RulePatch }>(
    ({ id, rule }) => {
      return apiPatch<Rule>(`/api/v1/admin/rules/${id}`, rule);
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
