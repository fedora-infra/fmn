// Severities in Fedora Messaging
export const DEBUG = { label: "debug", level: 10 };
export const INFO = { label: "info", level: 20 };
export const WARNING = { label: "warning", level: 30 };
export const ERROR = { label: "error", level: 40 };
export const SEVERITIES = [DEBUG, INFO, WARNING, ERROR];

// Tracking rules
export const TRACKING_RULES = [
  {
    name: "artifacts-owned",
    label: "Artifacts by users",
    prefixlabel: "Events related to the artifacts owned by the user",
    description:
      "Messages about artifacts (packages, modules, containers) that are owned by specific users",
  },
  {
    name: "artifacts-group-owned",
    label: "Artifacts by groups",
    prefixlabel: "Events related to the artifacts owned by the group",
    description:
      "Messages about artifacts (packages, modules, containers) that are owned by specific groups",
  },
  {
    name: "artifacts-followed",
    label: "Artifacts",
    prefixlabel: "Events related to the artifact",
    description:
      "Messages about specific artifacts (packages, modules, containers)",
  },
  {
    name: "related-events",
    label: "My Events",
    prefixlabel: "Events referring to me",
    description: "Events referring to me or affecting me",
  },
  {
    name: "users-followed",
    label: "Started by users",
    prefixlabel: "Events started by the user",
    description: "Events started by specific users",
  },
];
