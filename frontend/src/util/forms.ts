import { createInput, defaultConfig } from "@formkit/vue";
import MultiselectInput from "../components/MultiselectInput.vue";

const multiselect = createInput(MultiselectInput, {
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

export const config = defaultConfig({
  inputs: {
    multiselect,
  },
});
