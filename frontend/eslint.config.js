// vim: et ts=4 sw=4:
// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import pluginVue from "eslint-plugin-vue";
import {
  defineConfigWithVueTs,
  vueTsConfigs,
} from "@vue/eslint-config-typescript";
import eslintPluginPrettierRecommended from "eslint-plugin-prettier/recommended";

export default defineConfigWithVueTs(
  pluginVue.configs["flat/essential"],
  //pluginVue.configs['flat/strongly-recommended'],
  //pluginVue.configs['flat/recommended'],
  vueTsConfigs.recommended,
  eslintPluginPrettierRecommended,
  {
    ignores: ["src/api/generated.ts", "dist/*"],
  },
);
