// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import type { FormKitGroupValue } from "@formkit/core";
import type { RulePatch } from "../api/types";

interface RulePatchFormData extends RulePatch {
  id?: string;
}

export function formDataToRuleMutation(data: FormKitGroupValue) {
  const { id, ...rule } = data as RulePatchFormData;
  if (!id) {
    throw Error("No rule ID");
  }
  return { id: parseInt(id), rule };
}
