import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);
import { webSocket as RxWebSocket } from "rxjs/webSocket";
import { retryWhen } from "rxjs/operators";

export const lobby = {
  namespaced: true
};

export const jong = {
  namespaced: true,
  state: {
    
  },
  actions: {

  },
  mutations: {
    
  }
}

export const connection = {
  namespaced: true,
  state: {
    socket: null
  },
  actions: {
    join_room() {}
  },
  mutations: {
    new_conn(state, sk) {
      if (state.socket) {
        state.socket.unsubscribe();
        state.socket = null;
      }
      state.socket = sk;
    },
    disconnect(state) {
      if (state.socket) {
        state.socket.unsubscribe();
        state.socket = null;
      }
    }
  }
};

export const store = new Vuex.Store({
  modules: {
    lobby,
    connection
  },
  state: {
    skip_claim: false,
    hover_tile_id: null
  },
  mutations: {
    hover_tile(state, value = null) {
      state.hover_tile_id = value;
    },
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
