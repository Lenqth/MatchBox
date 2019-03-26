<template>
  <div>
    <v-content>
      <v-flex class="room-root">
        <transition-group name="roomtr">
          <roombox
            class="room-item"
            v-for="(item,index) in rlist"
            :key="index+1"
            :room="item"
            @dblclick.native="joinRoom(item)"
          />
        </transition-group>
      </v-flex>
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
import Vuetify from "vuetify";
import { webSocket as RxWebSocket } from "rxjs/webSocket";
import * as operators from "rxjs/operators";
import { interval } from "rxjs";

Vue.use(Vuetify);

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
    return { rlist: [], dialogOpen: false, socket: null, polling: null };
  },
  methods: {
    openModal() {
      this.$refs.newroom_dialog.open();
    },
    autoMatch() {
      this.$router.push("/room");
    },
    joinRoom(room) {
      var host = location.host;
      var _this = this;
      var socket = (window.socket = new RxWebSocket(
        "ws://" + host + "/ws/jong/room/join/" + room.room_id
      ));
      _this.$store.commit("connection/new_conn", socket);
      this.$router.push("/room");
    },
    reconnect() {
      this.disconnect();
      var send_sock = new RxWebSocket(
        "ws://" + location.host + "/ws/jong/lobby"
      );
      var _this = this;
      var sock = send_sock
        .pipe(
          operators.retryWhen(x =>
            x.pipe(
              operators.mergeMap((e, i) => {
                if (i > 3) {
                  return throwError(e);
                }
                return timer(1000).pipe(
                  operators.flatMap(async x => {
                    await _this.reconnect();
                    return x;
                  })
                );
              })
            )
          )
        )
        .subscribe(function(data) {
          //console.log("polling")
          //console.log(data)
          _this.rlist = data.rooms;
        });
      this.socket = sock;
      this.polling = interval(5000)
        .pipe(operators.map(x => ({ type: "polling" })))
        .subscribe(send_sock);
    },
    disconnect() {
      if (this.polling) {
        this.polling.unsubscribe();
        this.polling = null;
      }
    }
  },
  mounted() {
    this.$store.commit("connection/disconnect")
    this.reconnect();
  },
  beforeRouteLeave(to, from, next) {
    this.disconnect();
    next();
  }
};
</script>
<style>
.col1 {
  width: 60%;
}
#output {
  width: 80%;
  height: 40%;
}

.room-root {
  margin: 25px;
}

.room-container {
  display: flex;
  width: 80%;
  border: 1px lightcyan solid;
  margin: 10px;
  border: 2px black solid;
}

.roomtr-enter-active,
.roomtr-leave-active {
  transition: opacity 0.5s;
}
.roomtr-enter,
.roomtr-leave-to {
  opacity: 0;
}
</style>
