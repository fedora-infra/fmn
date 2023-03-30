// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import * as fs from "fs";

import { defineConfig } from "vite";
import { config as baseConfig } from "./vite.config";

// https://vitejs.dev/config/
const config: typeof baseConfig = {
  ...baseConfig,
  clearScreen: false,
  server: {
    watch: baseConfig.server?.watch,
    https: {
      key: fs.readFileSync("/etc/pki/tls/private/server.key"),
      cert: fs.readFileSync("/etc/pki/tls/certs/server.pem"),
    },
  },
};

export default defineConfig(config);
