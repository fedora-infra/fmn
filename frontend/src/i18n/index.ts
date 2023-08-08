// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { createI18n, type Composer } from "vue-i18n";

// import enUS from './locales/en-US.json'
//import messages from "@intlify/unplugin-vue-i18n/messages";

export const getLocale = (i18n: Composer) => {
  const selectedLocales = navigator.languages.filter((name) =>
    i18n.availableLocales.includes(name),
  );
  return selectedLocales ? selectedLocales[0] : navigator.language;
};

export const setLocale = (i18n: Composer) => {
  i18n.locale.value = getLocale(i18n);
};

const i18n = createI18n({
  legacy: false,
  locale: navigator.language,
  fallbackLocale: "en-US",
  messages: {},
  fallbackWarn: false,
  missingWarn: false,
});

export default i18n;
