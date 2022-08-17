import type { TrackingRule } from "./types";

// Severities in Fedora Messaging
export const DEBUG = { label: "debug", level: 10 };
export const INFO = { label: "info", level: 20 };
export const WARNING = { label: "warning", level: 30 };
export const ERROR = { label: "error", level: 40 };
export const SEVERITIES = [DEBUG, INFO, WARNING, ERROR];

// Tracking rules
export const TRACKING_RULES: TrackingRule[] = [
  {
    name: "artifact-owned",
    label: "Artifacts owned by me",
    description: "Artifacts (rpms, modules, containers) that are owned by me",
  },
  {
    name: "artifact-group-owned",
    label: "Artifacts owned by one of my groups",
    description:
      "Artifacts (rpms, modules, containers) that are owned by one of my groups",
  },
  {
    name: "artifact-followed",
    label: "Artifacts I follow",
    description: "Artifacts I follow",
  },
  {
    name: "related-events",
    label: "Events referring to me",
    description: "Events referring to me",
  },
  {
    name: "user-followed",
    label: "Users I follow",
    description: "Users I follow",
  },
];
export const TRACKING_RULES_2: { [key: string]: TrackingRule } = {
  "artifact-owned": {
    name: "artifact-owned",
    label: "Artifacts owned by me",
    description: "Artifacts (rpms, modules, containers) that are owned by me",
  },
  "artifact-group-owned": {
    name: "artifact-group-owned",
    label: "Artifacts owned by one of my groups",
    description:
      "Artifacts (rpms, modules, containers) that are owned by one of my groups",
  },
  "artifact-followed": {
    name: "artifact-followed",
    label: "Artifacts I follow",
    description: "Artifacts I follow",
  },
  "related-events": {
    name: "related-events",
    label: "Events referring to me",
    description: "Events referring to me",
  },
  "user-followed": {
    name: "user-followed",
    label: "Users I follow",
    description: "Users I follow",
  },
};
