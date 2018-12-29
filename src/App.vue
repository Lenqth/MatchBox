<template>
  <v-app id="root">
    <login/>
    <router-view id="app"/>
  </v-app>
</template>

<script>
import Vue from "vue";
import Vuetify from "vuetify";
import Vuex from "vuex";
Vue.use(Vuetify);
Vue.use(Vuex)

const store = new Vuex.Store({
  modules:{},
  state: {
    skip_claim: false
  },
  mutations: {
    skip_claim (state , value = "toggle") {
      if(value=="toggle"){
        state.skip_claim = !state.skip_claim;
      }else{
        state.skip_claim = value
      }
    },
    reset(state ){
      state.skip_claim = false;
    }
  }
})

import Login from "./components/login";
Vue.component("login", Login);

export default {
  name: "App",
  store
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
