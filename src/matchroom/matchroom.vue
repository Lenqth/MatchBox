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

import {webSocket as RxWebSocket} from 'rxjs/webSocket'
import * as utils from "./components/utils.js";
import memberbox from "./components/memberbox.vue";
Vue.component("memberbox", memberbox);

var audio1 = document.getElementById("sound1");

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
      socket.next( { ready: this.player_slot[this.you].ready } );
    },
    new_socket() {
      var host = location.host;
      var socket = (window.socket = new RxWebSocket(
        "ws://" + host + "/ws/jong/room/auto"
      ));
      socket.subscribe( this.onmessage , this.h_onerror , this.h_onclose );      
      this.$store.commit("connection/new_conn",socket)
      return socket;
    },
    onmessage(data) {
      if ("message" in data) {
        //    utils.play_sound("../assets/puu79_a.wav");
        setTimeout( function(){ var s1 = document.getElementById("sound1");
            if (s1) {
              s1.play();
            }
          } , 100 );
        this.add_message(data.message);
      }
      if ("roomsize" in data) {
        this.player_slot = new Array(data.roomsize).fill(0).map(function() {
          return { joined: false, ready: false, you: false, name: "none" };
        });
      }
      if ("position" in data) {
        this.player_slot[data.position].you = true;
        this.you = data.position;
        for (var [i, v] in data.room) {
          this.player_slot[i].joined = true;
        }
      }
      if ("room" in data) {
        for (var v of data.room) {
          this.player_slot[v.position].joined = true;
          this.player_slot[v.position].ready = v.ready;
        }
      }
      if ("joined" in data) {
        var dat = data.joined;
        this.player_slot[dat.position].joined = true;
        this.player_slot[dat.position].ready = dat.ready;
      }
      if ("exited" in data) {
        var dat = data.exited;
        this.player_slot[dat.position].joined = false;
      }
      if ("set_state" in data) {
        var stt = data.set_state;
        var pos = stt.pos;
        delete stt.pos;
        for (var key in stt) {
          this.player_slot[pos][key] = stt[key];
        }
      }
      if ("start" in data) {
        this.game_start(data.start);
      }
    },
    add_message(x) {
      this.messages.push(x);
    },
    h_onerror(e) {
      console.log("error:", e);
    },
    h_onclose(e) {
      console.log("close:", e);
      this.error_disp("connection closed. please reload later.");
      for (var x of document.getElementsByClassName("group-content")) {
        x.classList.remove("joined");
        x.classList.remove("group-content-you");
      }
    },
    game_start(arg) {
      this.$router.push("/jong");
    }
  },
  beforeRouteEnter(route, redirect, next) {
    next(vm => {
      let sk = vm.$store.state.connection.socket ;
      if ( sk == null ) {
        vm.new_socket();
      } else {
        sk.subscribe(vm.onmessage,vm.h_onerror,vm.h_onclose);
      }
    });
  }
};
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
