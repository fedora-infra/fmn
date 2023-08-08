// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { useQuery } from "@tanstack/vue-query";
import type { Ref } from "vue";
import type { operations } from "./generated";
import { apiGet } from "./index";

// Get all rules
export const useArtifactsQuery = (
  users: Ref<string[] | undefined> | undefined,
  groups: Ref<string[] | undefined> | undefined,
) => {
  const url = "/api/v1/artifacts";

  type OpType = operations["get_artifacts_api_v1_artifacts_get"];
  type OutputType = OpType["responses"][200]["content"]["application/json"];
  type ErrorType = OpType["responses"][422]["content"]["application/json"];

  const queryParams = { users, groups };
  const visible =
    (groups && groups.value && groups.value.length > 0) ||
    (users && users.value && users.value.length > 0);
  return useQuery<OutputType, ErrorType>(
    [url, queryParams],
    apiGet<OutputType>,
    { enabled: visible },
  );
};
