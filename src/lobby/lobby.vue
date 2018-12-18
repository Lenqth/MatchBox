<template>
  <div>
    <div class="room-root">
      <div class="room-container" id="roomlist">
        <roombox class="room-item" v-for="(item,index) in rlist" v-bind:room="item" :key="index" v-on:dblclick.native="joinRoom(item)"  />
      </div>
      <div class="footer">
        <button v-on:click="openModal()">ルームを新規作成</button>
        <button v-on:click="autoMatch()">おまかせマッチ</button>
      </div>
    </div>
    <div v-if="dialogOpen" class="modal">
      <newroom/>
    </div>
  </div>
</template>
<script>
import Vue from "vue";

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
      this.dialogOpen = true;
    },
    toggleModal() {
      this.dialogOpen = !this.dialogOpen;
    },
    autoMatch() {
      this.$router.push("/room");
    },
    async joinRoom(room){
      console.log("nyan");
      var host = location.host;
      if (location.port == 8080) {
        host = location.hostname + ":8000";
      }
      await new Promise( function(res,rej){
        var socket = (window.socket = new WebSocket(
          "ws://" + host + "/jong/room/join/" + room.room_id
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
      __vm = vm;
      if (window.socket) {
        window.socket.close();
      }
      new_socket(vm);
    });
  }
};

function new_socket(root) {
  var host = location.host;
  if (location.port == 8080) {
    host = location.hostname + ":8000";
  }
  var socket = (window.socket = new WebSocket("ws://" + host + "/jong/lobby"));
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
