// vim: et ts=4 sw=4:
// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import js from "@eslint/js";
import pluginVue from 'eslint-plugin-vue'
import vueTsEslintConfig from "@vue/eslint-config-typescript";
import prettierConfig from "@vue/eslint-config-prettier";
//import skipFormattingConfig from "@vue/eslint-config-prettier/skip-formatting";

export default [
    js.configs.recommended,
    ...pluginVue.configs['flat/essential'],
    //...pluginVue.configs['flat/strongly-recommended'],
    //...pluginVue.configs['flat/recommended'],
    ...vueTsEslintConfig(),
    {
        plugins: {
            prettier: prettierConfig,
            //prettier: skipFormattingConfig,
        },
    },
    {
        ignores: ["src/api/generated.ts", "dist/*"],
    },
];
