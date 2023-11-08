// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { useUserStore } from "@/stores/user";
import {
  useMutation,
  useQuery,
  useQueryClient,
  type UseMutationReturnType,
  type UseQueryReturnType,
} from "@tanstack/vue-query";
import type { Ref } from "vue";
import type { paths } from "./generated";
import { apiDelete, apiGet, apiPatch, apiPost, apiPut } from "./index";

// Get all rules
type RulesOpType = paths["/api/v1/users/{username}/rules"]["get"];
type RulesOutputType =
  RulesOpType["responses"][200]["content"]["application/json"];
type RulesErrorType =
  RulesOpType["responses"][422]["content"]["application/json"];
export const useRulesQuery = (): UseQueryReturnType<
  RulesOutputType,
  RulesErrorType
> => {
  const userStore = useUserStore();
  const url = `/api/v1/users/${userStore.username}/rules`;
  return useQuery({
    queryKey: [url],
    queryFn: apiGet<RulesOutputType>,
    enabled: userStore.loggedIn,
  });
};

// Get a rule
type RuleOpType = paths["/api/v1/users/{username}/rules/{id}"]["get"];
type RuleOutputType =
  RuleOpType["responses"][200]["content"]["application/json"];
type RuleErrorType =
  RuleOpType["responses"][422]["content"]["application/json"];
export const useRuleQuery = (
  id: number,
): UseQueryReturnType<RuleOutputType, RuleErrorType> => {
  const userStore = useUserStore();
  const url = `/api/v1/users/${userStore.username}/rules/${id}`;
  return useQuery({ queryKey: [url], queryFn: apiGet<RuleOutputType> });
};

// Add a new rule
type AddRuleOpType = paths["/api/v1/users/{username}/rules"]["post"];
type AddRuleBodyType =
  AddRuleOpType["requestBody"]["content"]["application/json"];
type AddRuleOutputType =
  AddRuleOpType["responses"][200]["content"]["application/json"];
type AddRuleErrorType =
  AddRuleOpType["responses"][422]["content"]["application/json"];
export const useAddRuleMutation = (): UseMutationReturnType<
  AddRuleOutputType,
  AddRuleErrorType,
  AddRuleBodyType,
  unknown
> => {
  const userStore = useUserStore();
  const client = useQueryClient();
  return useMutation({
    mutationFn: (data) =>
      apiPost<AddRuleOutputType, AddRuleBodyType>(
        `/api/v1/users/${userStore.username}/rules`,
        data,
      ),

    onSuccess: async () => {
      await client.invalidateQueries({
        queryKey: [`/api/v1/users/${userStore.username}/rules`],
      });
    },
  });
};

// Edit a rule
type EditRuleOpType = paths["/api/v1/users/{username}/rules/{id}"]["put"];
type EditRuleOutputType =
  EditRuleOpType["responses"][200]["content"]["application/json"];
type EditRuleErrorType =
  EditRuleOpType["responses"][422]["content"]["application/json"];
export const useEditRuleMutation = (
  id: number,
): UseMutationReturnType<
  EditRuleOutputType,
  EditRuleErrorType,
  EditRuleOutputType,
  unknown
> => {
  const userStore = useUserStore();
  const client = useQueryClient();
  const url = `/api/v1/users/${userStore.username}/rules/${id}`;
  return useMutation({
    mutationFn: (data: EditRuleOutputType) =>
      apiPut<EditRuleOutputType>(url, data),

    onSuccess: async () => {
      await client.invalidateQueries({ queryKey: [url] });
      await client.invalidateQueries({
        queryKey: [`/api/v1/users/${userStore.username}/rules`],
      });
    },
  });
};

// Delete a rule
type DeleteRuleOpType = paths["/api/v1/users/{username}/rules/{id}"]["delete"];
type DeleteRuleOutputType = DeleteRuleOpType["parameters"]["path"]["id"];
type DeleteRuleErrorType =
  DeleteRuleOpType["responses"][422]["content"]["application/json"];
export const useDeleteRuleMutation = (): UseMutationReturnType<
  void,
  DeleteRuleErrorType,
  DeleteRuleOutputType,
  unknown
> => {
  const userStore = useUserStore();
  const client = useQueryClient();
  return useMutation({
    mutationFn: (id) =>
      apiDelete(`/api/v1/users/${userStore.username}/rules/${id}`),

    onSuccess: async () => {
      const url = `/api/v1/users/${userStore.username}/rules`;
      await client.invalidateQueries({
        queryKey: [url],
        refetchType: "active",
      });
    },
  });
};

/*
 * Admin
 */

// Get all rules
type AdminRulesOpType = paths["/api/v1/admin/rules"]["get"];
type AdminRulesOutputType =
  AdminRulesOpType["responses"][200]["content"]["application/json"];
type AdminRulesErrorType =
  AdminRulesOpType["responses"][422]["content"]["application/json"];
export const useAdminRulesQuery = (
  username: Ref<string>,
): UseQueryReturnType<AdminRulesOutputType, AdminRulesErrorType> => {
  const url = `/api/v1/admin/rules`;
  return useQuery({
    queryKey: [url, { username }],
    queryFn: apiGet<AdminRulesOutputType>,
  });
};

// Get disabled rules
type DisabledRulesOpType = paths["/api/v1/admin/rules"]["get"];
type DisabledRulesOutputType =
  DisabledRulesOpType["responses"][200]["content"]["application/json"];
type DisabledRulesErrorType =
  DisabledRulesOpType["responses"][422]["content"]["application/json"];
export const useDisabledRulesQuery = (): UseQueryReturnType<
  DisabledRulesOutputType,
  DisabledRulesErrorType
> => {
  const url = "/api/v1/admin/rules";
  return useQuery({
    queryKey: [url, { disabled: true }],
    queryFn: apiGet<DisabledRulesOutputType>,
  });
};

// Patch an existing rule
type PatchRuleOpType = paths["/api/v1/admin/rules/{id}"]["patch"];
type PatchRuleBodyType =
  PatchRuleOpType["requestBody"]["content"]["application/json"];
type PatchRuleOutputType =
  PatchRuleOpType["responses"][200]["content"]["application/json"];
type PatchRuleFnOutputType = {
  id: PatchRuleOpType["parameters"]["path"]["id"];
  rule: PatchRuleBodyType;
};
type PatchRuleErrorType =
  PatchRuleOpType["responses"][422]["content"]["application/json"];
export const usePatchRuleMutation = (): UseMutationReturnType<
  PatchRuleOutputType,
  PatchRuleErrorType,
  PatchRuleFnOutputType,
  unknown
> => {
  const client = useQueryClient();
  return useMutation({
    mutationFn: ({ id, rule }) => {
      return apiPatch<PatchRuleOutputType, PatchRuleBodyType>(
        `/api/v1/admin/rules/${id}`,
        rule,
      );
    },

    onSuccess: async () => {
      await client.invalidateQueries({
        queryKey: [
          "/api/v1/admin/rules",
          {
            disabled: true,
          },
        ],
      });
    },
  });
};
