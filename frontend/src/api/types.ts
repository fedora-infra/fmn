// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import type { AxiosError } from "axios";
import type { DEBUG, ERROR, INFO, WARNING } from "./constants";
import type { components } from "./generated";

export interface SelectOption<T> {
  label: string;
  value: T;
}

export type Severity =
  | typeof DEBUG
  | typeof INFO
  | typeof WARNING
  | typeof ERROR;

export type Destination = components["schemas"]["Destination"];
export type Filters = components["schemas"]["Filters"];
export type User = components["schemas"]["User"];
export type Artifact = components["schemas"]["Artifact"];
export type GenerationRule = components["schemas"]["GenerationRule"];
export type Rule = components["schemas"]["Rule"];
export type NewRule = components["schemas"]["NewRule"];
export type RulePatch = components["schemas"]["RulePatch"];
export type HTTPValidationError = components["schemas"]["HTTPValidationError"];
export interface PostError {
  detail?: HTTPValidationError["detail"] | string;
}
export type APIError = AxiosError<{ detail: string }>;
