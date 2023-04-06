<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

<script setup lang="ts">
import { useUserStore } from "@/stores/user";

const api_docs_url = import.meta.env.VITE_API_URL + "/docs";
const version = import.meta.env.VITE_VERSION;

const userStore = useUserStore();
</script>

<template>
  <footer class="footer">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col text-center">
          Powered by Fedora Message Notifications (FMN)
        </div>
      </div>
      <div class="row justify-content-center">
        <div class="col text-center">
          <a href="https://github.com/fedora-infra/fmn/issues/new"
            >Report Issue</a
          >
          <template v-if="userStore.isAdmin">
            | <a :href="api_docs_url">FMN API Documentation</a>
          </template>
        </div>
      </div>
      <div v-if="version" class="row justify-content-center">
        <div class="col text-center text-white-50">Version {{ version }}</div>
      </div>
      <div
        class="row justify-content-center border-top border-secondary mt-4 pt-3 text-center"
      >
        <div class="col-sm-3 col-4 mt-3">
          <div>
            <dl>
              <dt class="text-uppercase h5"><strong>About</strong></dt>
              <dd><a href="https://getfedora.org/">Get Fedora Linux</a></dd>
              <dd><a href="https://getfedora.org/en/sponsors/">Sponsors</a></dd>
              <dd><a href="https://fedoramagazine.org">Fedora Magazine</a></dd>
              <dd>
                <a href="https://fedoraproject.org/wiki/Legal:Main#Legal"
                  >Legal</a
                >
              </dd>
            </dl>
          </div>
        </div>
        <div class="col-sm-3 col-4 mt-3">
          <div>
            <dl>
              <dt class="text-uppercase h5"><strong>Support</strong></dt>
              <dd>
                <a
                  href="https://fedoraproject.org/wiki/Communicating_and_getting_help"
                  >Get Help</a
                >
              </dd>
              <dd><a href="https://ask.fedoraproject.org/">Ask Fedora</a></dd>
              <dd>
                <a href="https://fedoraproject.org/wiki/Common_F33_bugs"
                  >Common Bugs</a
                >
              </dd>
              <dd>
                <a href="https://developer.fedoraproject.org/"
                  >Fedora Developer Portal</a
                >
              </dd>
            </dl>
          </div>
        </div>
        <div class="col-sm-3 col-4 mt-3">
          <div>
            <dl>
              <dt class="text-uppercase h5"><strong>Community</strong></dt>
              <dd>
                <a href="https://fedoraproject.org/wiki/Join">Join Fedora</a>
              </dd>
              <dd>
                <a href="https://fedoraproject.org/wiki/Overview"
                  >About Fedora</a
                >
              </dd>
              <dd><a href="http://fedoraplanet.org">Planet Fedora</a></dd>
              <dd>
                <a href="https://accounts.fedoraproject.org/"
                  >Fedora Accounts</a
                >
              </dd>
            </dl>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-12 text-center mt-3">
          <p>
            Fedora is sponsored by Red Hat.
            <a
              href="https://www.redhat.com/en/technologies/linux-platforms/articles/relationship-between-fedora-and-rhel"
              >Learn more about the relationship between Red Hat and Fedora »</a
            >
          </p>
          <div class="py-3">
            <a class="border-0" href="https://www.redhat.com/"
              ><img
                class="rh-logo"
                src="@/assets/redhat-logo.png"
                alt="Red Hat Logo"
            /></a>
          </div>
          <p>© 2023 Red Hat, Inc. and others.</p>
        </div>
      </div>
    </div>
  </footer>
</template>

<style>
body {
  position: relative;
  min-height: 100vh;
}

.footer {
  bottom: 0;
  position: absolute;
  width: 100%;
  height: 30rem;
}

.container.main {
  padding-bottom: 33rem;
}
</style>
