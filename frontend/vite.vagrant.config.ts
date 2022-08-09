import { fileURLToPath, URL } from "url";
import * as fs from "fs";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  clearScreen: false,
  server: {
    watch: {
      usePolling: true,
    },
    https: {
      key: fs.readFileSync("/etc/pki/tls/private/server.key"),
      cert: fs.readFileSync("/etc/pki/tls/certs/server.pem"),
    },
  },
});
