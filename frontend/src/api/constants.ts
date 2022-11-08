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
    name: "artifacts-owned",
    label: "Artifacts owned by specific users",
    description:
      "Messages about artifacts (packages, modules, containers) that are owned by specific users",
  },
  {
    name: "artifacts-group-owned",
    label: "Artifacts owned by specific groups",
    description:
      "Messages about artifacts (packages, modules, containers) that are owned by specific groups",
  },
  {
    name: "artifacts-followed",
    label: "Artifacts I follow",
    description:
      "Messages about specific artifacts (packages, modules, containers)",
  },
  {
    name: "related-events",
    label: "Events referring to me",
    description: "Events referring to me or affecting me",
  },
  {
    name: "users-followed",
    label: "Users I follow",
    description: "Users whose actions I follow",
  },
];
