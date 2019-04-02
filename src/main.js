// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import Vuetify from "vuetify";
import Vuex from "vuex";
Vue.use(Vuetify);
Vue.use(Vuex);
import "vuetify/dist/vuetify.min.css";
import "material-design-icons-iconfont/dist/material-design-icons.css";
Vue.config.productionTip = false;

import App from "./App";
import router from "./router";
import { store } from "./vuex_stores/root";

/* eslint-disable no-new */
new Vue({
  el: "#app",
  store,
  router,
  components: { App },
  template: "<App/>"
});
