import { plugin as FormKitPlugin } from "@formkit/vue";
import { createPinia } from "pinia";
import { createApp } from "vue";
import { VueQueryPlugin } from "vue-query";

import App from "./App.vue";
import auth from "./auth";
import router from "./router";

import "./assets/main.css";

import "bootstrap";
import "fedora-bootstrap/dist/fedora-bootstrap.min.css";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(auth, { router });
app.use(VueQueryPlugin);
app.use(FormKitPlugin);

app.mount("#app");
