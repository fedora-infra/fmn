// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { useUserStore } from "@/stores/user";
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";
import type { Ref } from "vue";
import type { paths } from "./generated";
import { apiDelete, apiGet, apiPatch, apiPost, apiPut } from "./index";

// Get all rules
export const useRulesQuery = () => {
  const userStore = useUserStore();
  const url = `/api/v1/users/${userStore.username}/rules`;

  type OpType = paths["/api/v1/users/{username}/rules"]["get"];
  type OutputType = OpType["responses"][200]["content"]["application/json"];
  type ErrorType = OpType["responses"][422]["content"]["application/json"];

  return useQuery<OutputType, ErrorType>([url], apiGet<OutputType>, {
    enabled: userStore.loggedIn,
  });
};

// Get a rule
export const useRuleQuery = (id: number) => {
  const userStore = useUserStore();
  const url = `/api/v1/users/${userStore.username}/rules/${id}`;

  type OpType = paths["/api/v1/users/{username}/rules/{id}"]["get"];
  type OutputType = OpType["responses"][200]["content"]["application/json"];
  type ErrorType = OpType["responses"][422]["content"]["application/json"];

  return useQuery<OutputType, ErrorType>([url], apiGet<OutputType>);
};

// Add a new rule
export const useAddRuleMutation = () => {
  const userStore = useUserStore();
  const client = useQueryClient();

  type OpType = paths["/api/v1/users/{username}/rules"]["post"];
  type BodyType = OpType["requestBody"]["content"]["application/json"];
  type OutputType = OpType["responses"][200]["content"]["application/json"];
  type ErrorType = OpType["responses"][422]["content"]["application/json"];

  return useMutation<OutputType, ErrorType, BodyType>(
    (data) =>
      apiPost<OutputType, BodyType>(
        `/api/v1/users/${userStore.username}/rules`,
        data,
      ),
    {
      onSuccess: async () => {
        await client.invalidateQueries([
          `/api/v1/users/${userStore.username}/rules`,
        ]);
      },
    },
  );
};

// Edit a rule
export const useEditRuleMutation = (id: number) => {
  const userStore = useUserStore();
  const client = useQueryClient();
  const url = `/api/v1/users/${userStore.username}/rules/${id}`;

  type OpType = paths["/api/v1/users/{username}/rules/{id}"]["put"];
  type OutputType = OpType["responses"][200]["content"]["application/json"];
  type ErrorType = OpType["responses"][422]["content"]["application/json"];

  return useMutation<OutputType, ErrorType, OutputType>(
    (data: OutputType) => apiPut<OutputType>(url, data),
    {
      onSuccess: async () => {
        await client.invalidateQueries([url]);
        await client.invalidateQueries([
          `/api/v1/users/${userStore.username}/rules`,
        ]);
      },
    },
  );
};

// Delete a rule
export const useDeleteRuleMutation = () => {
  const userStore = useUserStore();
  const client = useQueryClient();

  type OpType = paths["/api/v1/users/{username}/rules/{id}"]["delete"];
  type ErrorType = OpType["responses"][422]["content"]["application/json"];

  return useMutation<void, ErrorType, OpType["parameters"]["path"]["id"]>(
    (id) => apiDelete(`/api/v1/users/${userStore.username}/rules/${id}`),
    {
      onSuccess: async () => {
        const url = `/api/v1/users/${userStore.username}/rules`;
        await client.invalidateQueries([url], { refetchType: "active" });
      },
    },
  );
};

/*
 * Admin
 */

// Get all rules
export const useAdminRulesQuery = (username: Ref<string>) => {
  const url = `/api/v1/admin/rules`;

  type OpType = paths["/api/v1/admin/rules"]["get"];
  type OutputType = OpType["responses"][200]["content"]["application/json"];
  type ErrorType = OpType["responses"][422]["content"]["application/json"];

  return useQuery<OutputType, ErrorType>(
    [url, { username }],
    apiGet<OutputType>,
  );
};

// Get disabled rules
export const useDisabledRulesQuery = () => {
  const url = "/api/v1/admin/rules";

  type OpType = paths["/api/v1/admin/rules"]["get"];
  type OutputType = OpType["responses"][200]["content"]["application/json"];
  type ErrorType = OpType["responses"][422]["content"]["application/json"];
  return useQuery<OutputType, ErrorType>(
    [url, { disabled: true }],
    apiGet<OutputType>,
  );
};

// Patch an existing rule
export const usePatchRuleMutation = () => {
  const client = useQueryClient();

  type OpType = paths["/api/v1/admin/rules/{id}"]["patch"];
  type BodyType = OpType["requestBody"]["content"]["application/json"];
  type OutputType = OpType["responses"][200]["content"]["application/json"];
  type ErrorType = OpType["responses"][422]["content"]["application/json"];

  return useMutation<
    OutputType,
    ErrorType,
    { id: OpType["parameters"]["path"]["id"]; rule: BodyType }
  >(
    ({ id, rule }) => {
      return apiPatch<OutputType, BodyType>(`/api/v1/admin/rules/${id}`, rule);
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
    },
  );
};
