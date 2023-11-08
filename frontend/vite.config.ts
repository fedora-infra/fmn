// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

/// <reference types="vitest" />
import VueI18nPlugin from "@intlify/unplugin-vue-i18n/vite";
import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "url";
import { defineConfig, type UserConfig } from "vite";

// https://vitejs.dev/config/

export const config: UserConfig = {
  plugins: [
    vue(),
    VueI18nPlugin({
      globalSFCScope: true,
    }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    watch: {
      usePolling: true,
    },
  },
  test: {
    environment: "jsdom",
    testTimeout: 20000,
    setupFiles: ["./src/tests.ts"],
    globals: true,
    coverage: {
      reporter: ["text", "json", "html"],
      all: true,
      exclude: [
        "vite.config.ts",
        "vite.vagrant.config.ts",
        ".eslintrc.cjs",
        "env.d.ts",
        "src/main.ts",
        "src/api/generated.ts",
        "dist/**",
      ],
      // Uncomment to check thresholds:
      // lines: 90,
      // functions: 90,
      // branches: 90,
    },
  },
};

export default defineConfig(config);
