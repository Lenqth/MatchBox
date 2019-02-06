<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" min-width="290">
      <v-card>
        <v-card-title class="headline">部屋の作成</v-card-title>ゲーム:
        <select name="type" class="selection" v-model="__game_type" @change="getConfig()">
          <option
            v-for="(item,index) in game_type_option"
            v-bind:value="item.id"
            :key="index"
          >{{item.name}}</option>
        </select>
        <div class="dialog-body">
          <selection
            v-for="(item,index) in detail_options"
            :key="index"
            v-on:changed="(e) => Changed(index,e)"
            v-bind:title="item.display_name"
            v-bind:items="item.value"
            v-bind:default="item.default"
          />
        </div>
        <v-card-actions>
          <div class="dialog-footer">
            <v-btn @click="createRoom()">作成</v-btn>
          </div>
          <div class="dialog-exit">
            <v-btn @click="closeThis()">✕</v-btn>
          </div>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>
<script>
import Vue from "vue";
import axios from "axios";

import SelectionControl from "./selection.vue";
Vue.component("selection", SelectionControl);

var option = [
  { id: "jong", name: "中国麻雀" },
  { id: "nyan", name: "にゃんにゃん～" }
];
var selected_game_type = option[0].id;
export default {
  data: () => ({
    game_type: option[0].id,
    game_type_option: option,
    detail_options: {},
    detail_options_selected: {},
    dialog: false
  }),
  methods: {
    open() {
      this.dialog = true;
    },
    closeThis() {
      this.dialog = false;
    },
    Changed(index, e) {
      this.detail_options_selected[index] = e;
    },
    async getConfig() {
      var host = location.host;
      // if (location.port == 8080) { host = location.hostname + ":8000"; }
      var response = await axios.get(
        "http://" + host + "/api/config/" + this.game_type
      );
      console.log(response.data);
      this.detail_options = response.data;
      for (var index in this.detail_options) {
        this.detail_options_selected[index] = this.detail_options[
          index
        ].default;
      }
    },
    async createRoom() {
      var socket = await new_socket_conf();
      console.log("connected");
      var config = this.detail_options_selected;
      config.game_type = this.game_type;
      socket.send(JSON.stringify(this.detail_options_selected));
      this.$router.push("/room");
    }
  },
  computed: {
    __game_type: {
      get() {
        return this.game_type;
      },
      set(val) {
        Vue.set(this, "game_type", val);
      }
    }
  },
  created: function() {
    this.getConfig();
  }
};

function new_socket_conf() {
  return new Promise((res, rej) => {
    var host = location.host;
    var socket = (window.socket = new WebSocket(
      "ws://" + host + "/ws/jong/room/configured"
    ));
    window.socket.addEventListener(
      "open",
      () => {
        res(socket);
      },
      { once: true }
    );
  });
}
</script>
<style>
.dialog-room {
  position: relative;
  background-color: lightgray;
  width: 600px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
}
.selection {
  min-width: 200px;
}

.dialog-body {
  margin-top: 20px;
}
.dialog-footer {
  margin-top: 50px;
}
.dialog-exit {
  position: absolute;
  top: 5px;
  right: 5px;
}

.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}
</style>
