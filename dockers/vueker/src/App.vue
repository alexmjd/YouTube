<template>
  <div id="app" class="dark-theme h-100">
    <div :class="sx.app">
    <app-navbar></app-navbar>
    <router-view></router-view>
    </div>
  </div>
</template>

<script>
import AppNavbar from "./components/Navbar";

export default {
  components: { AppNavbar }
};
</script>

<style lang="scss" module="sx">
// @import "style/main.scss";

  html, body {
    margin : auto;
    height: 100%;
  }

  .app {
    width: 100%;
    height: 100vh;
    position: fixed;
  }
</style>
