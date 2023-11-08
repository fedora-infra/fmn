// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { useQuery, type UseQueryReturnType } from "@tanstack/vue-query";
import type { Ref } from "vue";
import type { operations } from "./generated";
import { apiGet } from "./index";

// Get all rules
type ArtifactsOpType = operations["get_artifacts_api_v1_artifacts_get"];
type ArtifactsOutputType =
  ArtifactsOpType["responses"][200]["content"]["application/json"];
type ArtifactsErrorType =
  ArtifactsOpType["responses"][422]["content"]["application/json"];
export const useArtifactsQuery = (
  users: Ref<string[] | undefined> | undefined,
  groups: Ref<string[] | undefined> | undefined,
): UseQueryReturnType<ArtifactsOutputType, ArtifactsErrorType> => {
  const url = "/api/v1/artifacts";
  const queryParams = { users, groups };
  const visible =
    (groups && groups.value && groups.value.length > 0) ||
    (users && users.value && users.value.length > 0);
  return useQuery({
    queryKey: [url, queryParams],
    queryFn: apiGet<ArtifactsOutputType>,
    enabled: visible,
  });
};
