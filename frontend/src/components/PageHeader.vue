<script setup lang="ts">
import HelloWorld from "./HelloWorld.vue";
import LoginButton from "./LoginButton.vue";
import MainNavLink from "./MainNavLink.vue";
</script>

<template>
  <header>
    <nav
      class="navbar navbar-expand-lg navbar-light masthead justify-content-between py-2"
    >
      <div class="container">
        <a class="navbar-brand" href="/"
          ><img
            src="@/assets/logo.png"
            alt="Fedora Account System logo"
            height="40"
        /></a>
        <ul class="navbar-nav fw-bold align-items-center">
          <MainNavLink to="/">Home</MainNavLink>
          <MainNavLink to="/about">About</MainNavLink>
          <MainNavLink to="/rules">Rules</MainNavLink>
          <MainNavLink to="/destinations">Destinations</MainNavLink>
          <LoginButton />
        </ul>
      </div>
    </nav>

    <div class="bg-light border-bottom py-5">
      <div class="container">
        <HelloWorld msg="You did it!!!" />
      </div>
    </div>
  </header>
</template>
