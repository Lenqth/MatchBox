<template>
  <v-content>
    <audio id="sound1" preload="auto">
      <source src="@/assets/sounds/puu79_a.wav" type="audio/wav">
    </audio>
    <v-layout row>
      <v-container>
        <transition-group name="message-card">
          <v-card v-for="(item,index) in messages" :key="index+1" style="margin:4px">{{item}}</v-card>
        </transition-group>
      </v-container>
      <v-container xs2>
        <memberbox v-bind:player_slot="player_slot" v-on:ready-changed="send_ready()"/>
      </v-container>
    </v-layout>
  </v-content>
</template>
<script>
import Vue from "vue";
import Vuetify from 'vuetify'
Vue.use(Vuetify);

import * as utils from "./components/utils.js";
import memberbox from "./components/memberbox.vue";
Vue.component("memberbox", memberbox);

var audio1 = document.getElementById("sound1");


function send(s) {
  var obj = { message: s };
  socket.send(JSON.stringify(obj));
}
var __vm = null;
export default {
  name: "MatchRoom",
  data(){
    return {
      player_slot: [], 
      messages : [],
      you : -1
    }
  },
  methods: {
    send_ready() {
      socket.send(JSON.stringify({ ready: this.player_slot[this.you].ready }));
    },
    new_socket() {
      var host = location.host;
      var socket = (window.socket = new WebSocket(
        "ws://" + host + "/ws/jong/room/auto"
      ));
      socket.onmessage = this.onmessage;
      socket.onerror = h_onerror;
      socket.onclose = h_onclose;
      return socket;
    },
    onmessage(e) {
      var o = JSON.parse(e.data);
      if ("message" in o) {
        //    utils.play_sound("../assets/puu79_a.wav");
        var s1 = document.getElementById("sound1");
        if (s1) {
          s1.play();
        }
        this.add_message(o.message);
      }
      if ("roomsize" in o) {
        this.player_slot = new Array(o.roomsize).fill(0).map(function() {
          return { joined: false, ready: false, you: false, name: "none" };
        });
      }
      if ("position" in o) {
        this.player_slot[o.position].you = true;
        this.you = o.position;
        for (var [i, v] in o.room) {
          this.player_slot[i].joined = true;
        }
      }
      if ("room" in o) {
        for (var v of o.room) {
          this.player_slot[v.position].joined = true;
          this.player_slot[v.position].ready = v.ready;
        }
      }
      if ("joined" in o) {
        var dat = o.joined;
        this.player_slot[dat.position].joined = true;
        this.player_slot[dat.position].ready = dat.ready;
      }
      if ("exited" in o) {
        var dat = o.exited;
        this.player_slot[dat.position].joined = false;
      }
      if ("set_state" in o) {
        var stt = o.set_state;
        var pos = stt.pos;
        delete stt.pos;
        for (var key in stt) {
          this.player_slot[pos][key] = stt[key];
        }
      }
      if ("start" in o) {
        game_start(o.start);
      }
    },
    add_message(x) {
      this.messages.push(x);
    }
  },
  beforeRouteEnter(route, redirect, next) {
    next(vm => {
      __vm = vm;
      if (!isRoomSocket(window.socket)) {
        vm.new_socket();
      } else {
        socket.onmessage = vm.onmessage;
        socket.onerror = h_onerror;
        socket.onclose = h_onclose;
      }
    });
  }
};
function isRoomSocket(socket) {
  if (!socket) return false;
  if (socket.url.indexOf("room") >= 0) {
    return true;
  }
  return false;
}

function h_onerror(e) {
  console.log("error:", e);
}
function h_onclose(e) {
  console.log("close:", e);
  this.error_disp("connection closed. please reload later.");
  for (var x of document.getElementsByClassName("group-content")) {
    x.classList.remove("joined");
    x.classList.remove("group-content-you");
  }
}

function game_start(arg) {
  __vm.$router.push("/jong");
}
</script>
<style scoped>
.room-root {
  margin: 25px;
}

.flexbox {
  display: flex;
}
.col1 {
  width: 60%;
}
.chat-output {
  width: 80%;
  height: 40%;
}

.message-card-enter-active,.message-card-leave-active {
  transition: opacity .5s;
}
.message-card-enter,.roomtr-leave-to{
  opacity: 0;
}


</style>
