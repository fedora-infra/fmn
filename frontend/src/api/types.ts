import type { DEBUG, ERROR, INFO, WARNING } from "./constants";

export interface TrackingRule {
  name: string;
  label: string;
  description: string;
}

export interface Destination {
  name: string;
  label: string;
  values: string[];
}

export interface Filter {
  name: string;
  title: string;
  choices?: string[];
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
  filters: Filter[];
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
  name: string;
  tracking_rule: TrackingRuleEditing;
  destinations: Destination[];
  filters: Filter[];
}

interface PostErrorDetail {
  loc: string[];
  msg: string;
  type: string;
}
export interface PostError {
  detail: PostErrorDetail[];
}
