// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import type { FormKitFrameworkContext, FormKitProps } from "@formkit/core";
import Multiselect from "@vueform/multiselect";

export const msProps = [
  "placeholder",
  "mode",
  "closeOnSelect",
  "filterResults",
  "resolveOnLoad",
  "minChars",
  "delay",
  "groups",
  "groupHideEmpty",
  "groupSelect",
  "searchable",
  "valueProp",
  "object",
  "class",
  "classes",
  "noOptionsText",
  "clearOnSearch",
];

interface FormKitMultiSelect extends Partial<Multiselect> {
  type: "multiselect";
  msOptions: Multiselect["options"];
  msLabel?: Multiselect["label"];
}
interface FormKitMultiSelectAsyncDefault
  extends Omit<FormKitMultiSelect, "type"> {
  type: "multiselectasyncdefault";
  msResultsToOptions?: (values: any[]) => Multiselect["options"][]; // eslint-disable-line @typescript-eslint/no-explicit-any
  msValueToOptions?: (values: any) => Multiselect["options"]; // eslint-disable-line @typescript-eslint/no-explicit-any
}

declare module "@formkit/inputs" {
  interface FormKitInputProps<Props extends FormKitInputs<Props>> {
    multiselect: FormKitMultiSelect;
    multiselectasyncdefault: FormKitMultiSelectAsyncDefault;
  }

  interface FormKitInputSlots<Props extends FormKitInputs<Props>> {
    multiselect: FormKitSelectSlots<Props>;
    multiselectasyncdefault: FormKitSelectSlots<Props>;
  }
}

export const getBindableProps = (context: FormKitFrameworkContext) => {
  const val: Partial<FormKitProps> = Object.keys(context.node.props)
    .filter((key) => msProps.includes(key))
    .reduce(
      (obj, key) => Object.assign(obj, { [key]: context.node.props[key] }),
      {},
    );
  val.id = context.id;
  val.name = context.name;
  val.value = context._value;
  val.disabled = context.disabled;
  val.options = context.node.props.msOptions;
  val.label = context.node.props.msLabel;
  return val;
};
