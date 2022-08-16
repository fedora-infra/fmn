export interface TrackingRule {
  name: string;
  title: string;
}

export interface Destination {
  name: string;
  title: string;
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

export interface Severity {
  name: string;
  level: number;
}
