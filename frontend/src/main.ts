import "@formkit/themes/genesis";
import { plugin as FormKitPlugin } from "@formkit/vue";
import { createApp } from "vue";
import { VueQueryPlugin } from "vue-query";
import { vueQueryPluginOptions } from "./api";
import App from "./App.vue";
import auth from "./auth";
import { config as formkitConfig } from "./forms";
import i18n from "./i18n";
import router from "./router";
import pinia from "./stores";

import "fedora-bootstrap/dist/fedora-bootstrap.min.css";
import "./assets/main.css";

const app = createApp(App);

app.use(pinia);
app.use(router);
app.use(auth, { router });
app.use(VueQueryPlugin, vueQueryPluginOptions);
app.use(FormKitPlugin, formkitConfig);
app.use(i18n);

app.mount("#app");
