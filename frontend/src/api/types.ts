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
  str_arg?: boolean;
}

export interface Application {
  name: string;
}

export type Severity =
  | typeof DEBUG
  | typeof INFO
  | typeof WARNING
  | typeof ERROR;

export interface Rule {
  name: string;
  tracking_rule: string;
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
