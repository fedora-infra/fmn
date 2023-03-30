// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { generateClasses } from "@formkit/themes";
import { createInput, defaultConfig } from "@formkit/vue";
import MultiSelectAsyncDefaultInput from "./MultiSelectAsyncDefaultInput.vue";
import MultiSelectInput from "./MultiSelectInput.vue";
import { msProps } from "./MultiSelectInputUtils";

// Define the multiselect Input for FormKit
const multiselect = createInput(MultiSelectInput, {
  props: [...msProps, "msOptions", "msLabel"],
});
const multiSelectAsyncDefault = createInput(MultiSelectAsyncDefaultInput, {
  props: [
    ...msProps,
    "msOptions",
    "msLabel",
    "msResultsToOptions",
    "msValueToOption",
  ],
});

// Create the FormKit config, including the multiselect input
export const config = defaultConfig({
  inputs: {
    multiselect,
    multiselectasyncdefault: multiSelectAsyncDefault,
  },
  config: {
    classes: generateClasses({
      global: {
        messages: "list-unstyled text-danger",
      },
      text: {
        outer: "$reset",
        input: "$reset form-control",
        label: "form-label",
        help: "text-muted",
      },
      select: {
        outer: "$reset",
        input: "$reset form-select",
      },
      submit: {
        outer: "$reset",
        input: "$reset btn btn-primary",
      },
      checkbox: {
        outer: "form-check form-switch",
        label: "form-check-label",
        input: "form-check-input",
        help: "text-muted",
      },
    }),
  },
});
