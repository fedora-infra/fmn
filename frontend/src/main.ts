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
import { vctooltip } from "@coreui/bootstrap-vue";

import "@coreui/coreui/dist/css/coreui.min.css";
import "fedora-bootstrap/dist/fedora-bootstrap.min.css";
import "./assets/main.css";

const app = createApp(App);

app.use(router);
app.use(auth, { router });
app.use(pinia);
app.use(VueQueryPlugin, vueQueryPluginOptions);
app.use(FormKitPlugin, formkitConfig);
app.use(i18n);
// Avoid a warning about the icons object not being provided.
app.provide("icons", {});

app.directive("c-tooltip", vctooltip);

app.mount("#app");
