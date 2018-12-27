<template>
  <div>
    <v-content>
      <div class="room-root">
        <v-flex id="roomlist">
          <roombox class="room-item" v-for="(item,index) in rlist" :key="index" :room="item" @dblclick.native="joinRoom(item)"/>
        </v-flex>
      </div>
    </v-content>
    <newroom ref="newroom_dialog"/>
    <v-footer dark height="auto">
      <v-card class="flex" flat tile>
        <v-card-title class="teal">
          <v-btn outline @click="openModal()">ルームを新規作成</v-btn>
          <v-btn outline @click="autoMatch()">おまかせマッチ</v-btn>
        </v-card-title>
      </v-card>
    </v-footer>
   </div>
</template>
<script>
import Vue from "vue";
import Vuetify from 'vuetify'
Vue.use(Vuetify);
import 'vuetify/dist/vuetify.min.css'

import * as utils from "./components/utils.js";

import newroomDialog from "./components/newroom.vue";
Vue.component("newroom", newroomDialog);

import roombox from "./components/roombox.vue";
Vue.component("roombox", roombox);

var audio1 = document.getElementById("sound1");

var __vm = null;

export default {
  name: "Lobby",
  data() {
    return { rlist: [], dialogOpen: false };
  },
  methods: {
    openModal() {
      this.$refs.newroom_dialog.open();
    },
    autoMatch() {
      this.$router.push("/room");
    },
    async joinRoom(room){
      var host = location.host;
      await new Promise( function(res,rej){
        var socket = (window.socket = new WebSocket(
          "ws://" + host + "/ws/jong/room/join/" + room.room_id
        ));
        window.socket.addEventListener(
          "open",
          () => {
            res(socket);
          },
          { once: true }
        ); } );
      this.$router.push("/room");
    }
  },
  beforeRouteEnter(route, redirect, next) {
    next(vm => {
      if (window.socket) {
        window.socket.close();
      }
      new_socket(vm);
    });
  }
};

function new_socket(root) {
  var host = location.host;
  //if (location.port == 8080) {host = location.hostname + ":8000";}
  var socket = (window.socket = new WebSocket("ws://" + host + "/ws/jong/lobby"));
  socket.onmessage = function(e) {
    var o = JSON.parse(e.data);
    console.log(o);
    root.rlist = o.rooms;
  };
}
</script>
<style>
.col1 {
  width: 60%;
}
#output {
  width: 80%;
  height: 40%;
}

.room-root{
  margin: 25px;
}

.room-container {
  display: flex;
  width: 80%;
  border: 1px lightcyan solid;
  margin: 10px;
  border: 2px black solid;
}

.room-item {
  box-sizing: border-box;
  flex-basis: 33.34%;
  flex-shrink: 1;
}

@keyframes blinkborder {
  0% {
    border-color: rgba(255, 255, 255, 1);
  }
  100% {
    border-color: rgba(255, 255, 255, 0.2);
  }
}

.room-item:nth-child(2n) {
  background-color: #eeeeee;
  /*flex-basis: 100%;*/
}
.room-item:nth-child(2n + 1) {
  background-color: #ccccdd;
  /*flex-basis: 100%;*/
}
</style>
