// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import type { FormKitFrameworkContext, FormKitProps } from "@formkit/core";

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

export const getBindableProps = (context: FormKitFrameworkContext) => {
  const val: Partial<FormKitProps> = Object.keys(context.node.props)
    .filter((key) => msProps.includes(key))
    .reduce(
      (obj, key) => Object.assign(obj, { [key]: context.node.props[key] }),
      {}
    );
  val.id = context.id;
  val.name = context.name;
  val.value = context._value;
  val.disabled = context.disabled;
  val.options = context.node.props.msOptions;
  val.label = context.node.props.msLabel;
  return val;
};
