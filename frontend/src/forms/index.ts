import { generateClasses } from "@formkit/themes";
import { createInput, defaultConfig } from "@formkit/vue";
import MultiSelectInput from "./MultiSelectInput.vue";

// Define the multiselect Input for FormKit
const multiselect = createInput(MultiSelectInput, {
  props: [
    "placeholder",
    "msOptions",
    "mode",
    "closeOnSelect",
    "groups",
    "groupHideEmpty",
    "searchable",
  ],
});

// Create the FormKit config, including the multiselect input
export const config = defaultConfig({
  inputs: {
    multiselect,
  },
  config: {
    classes: generateClasses({
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
        outer: "form-check",
        input: "form-check-input",
        label: "form-check-label",
        help: "text-muted",
      },
    }),
  },
});
