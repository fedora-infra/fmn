import type { DEBUG, ERROR, INFO, WARNING } from "./constants";

export interface TrackingRule {
  name: string;
  label: string;
  description: string;
}

export interface SelectOption<T> {
  label: string;
  value: T;
}

export interface Destination {
  protocol: string;
  address: string;
}

export interface DestinationGroup {
  name: string;
  label: string;
  values: SelectOption<Destination>[];
}

export interface Filter {
  applications?: string[];
  severities?: string[];
  my_actions?: boolean;
  topic?: string | null;
}

export interface Application {
  name: string;
}
export interface User {
  name: string;
}
export interface Group {
  name: string;
}
export interface Artifact {
  name: string;
}

export interface GenerationRule {
  id: number;
  destinations: Destination[];
  filters: Filter;
}

export type Severity =
  | typeof DEBUG
  | typeof INFO
  | typeof WARNING
  | typeof ERROR;

interface TrackingRuleEditing {
  name: string;
  params?: string[] | Record<string, string>;
}
export interface Rule {
  id: number;
  name: string;
  tracking_rule: TrackingRuleEditing;
  generation_rules: GenerationRule[];
}

interface PostErrorDetail {
  loc: string[];
  msg: string;
  type: string;
}
export interface PostError {
  detail: PostErrorDetail[];
}
