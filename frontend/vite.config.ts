/// <reference types="vitest" />
import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "url";
import { defineConfig, type UserConfig } from "vite";

// https://vitejs.dev/config/

export const config: UserConfig = {
  plugins: [vue()],
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
    coverage: {
      reporter: ["text", "json", "html"],
      all: true,
      exclude: [
        "vite.config.ts",
        "vite.vagrant.config.ts",
        ".eslintrc.cjs",
        "env.d.ts",
        "src/main.ts",
      ],
      // Uncomment to check thresholds:
      // lines: 90,
      // functions: 90,
      // branches: 90,
    },
  },
};

export default defineConfig(config);
