<template>
  <v-app id="root">
    <login/>
    <router-view id="app"/>
  </v-app>
</template>

<script>
import Vue from "vue";
import Vuetify from "vuetify";
Vue.use(Vuetify);

import Login from "./components/login";

Vue.component("login", Login);

export default {
  name: "App"
};
</script>
<style>
body{
  margin:0;
}
</style>
<style scoped>
#root{
  margin:0;
  height:100vh;
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0 0 0 0;
  height:calc(100vh - 40px);
}
</style>
