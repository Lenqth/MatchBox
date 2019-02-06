import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);
import { webSocket as RxWebSocket } from "rxjs/webSocket";
import { retryWhen } from "rxjs/operators";

export const lobby = {
  namespaced: true
};

export const store = new Vuex.Store({
  modules: {
    lobby
  },
  state: {
    skip_claim: false
  },
  mutations: {
    skip_claim(state, value = "toggle") {
      if (value == "toggle") {
        state.skip_claim = !state.skip_claim;
      } else {
        state.skip_claim = value;
      }
    },
    reset(state) {
      state.skip_claim = false;
    }
  }
});
