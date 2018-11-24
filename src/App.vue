<template>
  <div>
    <login/>
    <router-view id="app"/>
  </div>
</template>

<script>
import Vue from "vue";
import Login from "./components/login";

Vue.component("login", Login);

export default {
  name: "App"
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
