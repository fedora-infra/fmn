import type { DEBUG, ERROR, INFO, WARNING } from "./constants";

export interface TrackingRule {
  name: string;
  label: string;
  prefixlabel: string;
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
  type: "rpm" | "container" | "module" | "flatpak";
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

interface ListParamTrackingRule {
  name: "artifacts-owned" | "artifacts-group-owned" | "users-followed";
  params: string[];
}

interface NoParamTrackingRule {
  name: "related-events";
  params?: string;
}

interface ArtifactsFollowedTrackingRule {
  name: "artifacts-followed";
  params: Record<string, string>[];
}

export type TrackingRuleEditing =
  | ListParamTrackingRule
  | NoParamTrackingRule
  | ArtifactsFollowedTrackingRule;

export interface Rule {
  id: number;
  name: string;
  user: User;
  disabled: boolean;
  generated_last_week: number;
  tracking_rule: TrackingRuleEditing;
  generation_rules: GenerationRule[];
}

export type RuleCreation = Omit<Rule, "id" | "generated_last_week" | "user">;

export type RulePatch = Partial<Rule>;

interface PostErrorDetail {
  loc: string[];
  msg: string;
  type: string;
}
export interface PostError {
  detail: PostErrorDetail[] | string;
}

export interface NotificationContent {
  date: string;
  topic: string;
  summary: string;
  priority?: string;
  application?: string;
  author?: string;
}
export interface Notification {
  protocol: string;
  content: NotificationContent;
}
