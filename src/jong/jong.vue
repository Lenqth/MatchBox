<template>
  <div>
    <audio id="sound1" preload="auto">
      <source src="@/assets/sounds/puu79_a.wav" type="audio/wav">
    </audio>
    <audio id="sound2" preload="auto">
      <source src="@/assets/sounds/clock04.wav" type="audio/wav">
    </audio>
    <div class="jong-root">
      <div id="board-root" class="board-root">
        <div id="info">
          <p>ノコリ：{{ deck_left }}</p>
          <p>{{ get_wind_name( prev_wind ) }}場 {{ get_wind_name(seat_wind) }}風</p>
          <p v-if="time_left!=null">入力待機 残り：{{ time_left.toFixed(1) }}秒</p>
          <p>{{ message }}</p>
        </div>
        <player-area
          id="hand1"
          v-bind:player="players[(player_id+1)%4]"
          :open="open"
          class="player-field"
        />
        <player-area
          id="hand2"
          v-bind:player="players[(player_id+2)%4]"
          :open="open"
          class="player-field"
        />
        <player-area
          id="hand3"
          v-bind:player="players[(player_id+3)%4]"
          :open="open"
          class="player-field"
        />
        <player-area
          id="hand0"
          v-bind:player="players[player_id]"
          main="1"
          @tile="on_tile"
          @command="on_command"
          :open="open"
          class="player-field"
        />
      </div>
      <transition name="sideinfo">
        <div v-if="yakulist!=null" id="sideinfo">
          <yakulist :yakus="yakulist"/>
          <p style>計 : {{ calculated_score }}</p>
        </div>
      </transition>
    </div>
    <result-dialog v-model="result" @ok="ok()"/>
    <final-result-dialog :result="final_result" @ok="ok()"/>
  </div>
</template>

<script>
import Vue from "vue";
import {
  Hand,
  get_wind_name,
  numtosrc,
  relative_player_format
} from "./components/jong_network.js";
import * as utils from "./components/utils.js";

import PlayerArea from "./components/player.vue";
Vue.component("player-area", PlayerArea);

import Yakulist from "./components/yakulist.vue";
Vue.component("yakulist", Yakulist);

import Result from "./components/result.vue";
Vue.component("result-dialog", Result);

import FinalResult from "./components/final_result.vue";
Vue.component("final-result-dialog", FinalResult);

//import meld_selection from "./components/meld_selection.vue";
//Vue.component("meld-selection", meld_selection);

var deck = null;

function __img(x) {
  return '<img src="' + numtosrc(x) + '" >';
}

window.deck = deck;

export default {
  name: "Jong",
  data() {
    let obj = {};
    obj.players = new Array(4);
    obj.turn = 0;
    obj.nakimode = -1;
    obj.subturn = -1;
    obj.last_target = null;
    obj.deck_left = 0;
    obj.message = "*";
    obj.prev_wind = 0;
    obj.seat_wind = 0;
    obj.yakulist = null;
    obj.open = false;
    obj.calculated_score = "";
    obj.meld_selection = { type: "", tiles: [] };
    obj.result = null; // { player : "" , score : 0 , yaku : [] };
    obj.final_result = null;
    obj.player_id = 0;
    obj.time_left = null;
    obj.timeout = null;
    obj.input_resolve = null;
    for (let i = 0; i < 4; i++) {
      obj.players[i] = new Hand();
      obj.players[i].id = i;
    }
    return obj;
  },
  mounted() {
    this.start(window.socket);
  },
  methods: {
    numtosrc,
    get_wind_name: get_wind_name,
    on_tile(pos) {
      this.tile_click(pos);
    },
    on_command(type, pos) {
      this.command(type, pos);
    },
    tile_click(x) {
      var pl = this.players[this.player_id];
      var pos = x;
      if (this.input_resolve != null && pl.allow_discard) {
        this.input_resolve("discard", pos);
      }
    },
    command(type, pos) {
      if (this.input_resolve == null) {
        return;
      }
      this.input_resolve(type, pos);
    },
    async turn_input(cancelObj) {
      var _this = this;
      return new Promise(function(resolve) {
        _this.input_resolve = function(type, value) {
          var pl = this.players[this.player_id];
          if (type == "discard") {
            if (
              (pl.drawed != null && value == -1) ||
              (value >= 0 || value < pl.hand.length)
            ) {
              pl.trash_tile(value);
              _this.input_resolve = null;
              pl.allow_discard = false;
              resolve({ type: "discard", pos: value });
            }
          } else {
            _this.input_resolve = null;
            pl.allow_discard = false;
            resolve({ type: type, pos: value });
          }
        };
      });
    },
    async claim_input(cancelObj) {
      var _this = this;
      return new Promise(function(resolve) {
        _this.input_resolve = function(type, value) {
          _this.input_resolve = null;
          resolve({ type: type, pos: value });
        };
      });
    },
    timer_interval(resolve, timeout, cancelObj) {
      var left = (this.time_left =
        Math.floor((timeout - new Date().getTime()) / 100) / 10);
      if (left < 0) {
        resolve();
      }
      if (cancelObj.cancel) {
        resolve();
      }
    },
    async timer(timeout, cancelObj) {
      var cancel = null;
      await new Promise(resolve => {
        cancel = setInterval(
          () => this.timer_interval(resolve, timeout, cancelObj),
          100
        );
      });
      this.time_left = null;
      clearInterval(cancel);
      return null;
    },
    __last_target(t) {
      return this.last_target == t;
    },
    ok() {
      if (this.listener_ok != null) {
        this.listener_ok();
        this.listener_ok = null;
      }
    },
    assign(obj) {
      for (var k in obj) {
        if (k == "players") {
          for (var i = 0; i < 4; i++) {
            this.players[i].assign(obj.players[i]);
          }
        } else {
          this[k] = obj[k];
        }
      }
    },
    async resyncdata(conn) {
      this.conn = conn;
      this.$store.state.connection.socket.next({ type: "get_all" });
      var res = AsyncConnection.receiveAsync();
      this.assign(res);
    },
    async play_sound(id) {
      var el = document.getElementById(id);
      el.currentTime = 0;
      el.play();
    },
    async start(sock) {
      this.conn = this.$store.state.connection.socket;
      this.conn.next( { stand_by: "" } );
      var res = null;
      this.open = false;
      var proc = async ( res ) => {
        var pl = this.players[this.player_id];
        if (res.type === "reset") {
          delete res.type;
          this.$store.commit("reset");
          this.yakulist = null;
          this.calculated_score = null;
          this.assign(res);
          this.open = false;
          this.meld_selection = { type: "", tiles: [] };
          this.players[this.player_id].commands_available = [];
        }
        if (res.type === "agari") {
          this.result = { player: "", score: 0, tsumo: false, yaku: [] };
          this.result.player = relative_player_format(this.player_id, res.pid);
          this.result.score = res.yaku[0];
          this.result.yaku = res.yaku[1];
          this.result.tsumo = res.tsumo;
        }
        if (res.type === "gameover") {
          this.result = { player: "", score: 0, tsumo: false, yaku: [] };
          this.result.player = -1;
          this.result.score = 0;
          this.result.yaku = [];
          this.open = true;
        }
        if (res.type === "final_result") {
          this.final_result = res.dat;
        }
        if (res.type === "open_hand") {
          var hands = res.hand;
          for (let i = 0; i < 4; i++) {
            let p = hands[i];
            this.players[i].hand = p.hand;
            this.players[i].drawed = p.drew;
            this.open = true;
          }
        }
        if (res.type === "deck_left") {
          this.deck_left = res.deck_left;
        }
        if (res.type === "claim_command") {
          // {"commands_available": [{"type": 1, "pos": [[1], [2]]}], "_m_id": 7, "timeout": 1539616054.5650032}
          let tg_pl = res.target.player,
            tg_apkong = res.target.apkong,
            tg_tile = res.target.tile;
          this.players[this.player_id].hand = res.hand_tiles;
          this.players[this.player_id].drawed = null;
          this.players[tg_pl].target = tg_apkong ? "apkong" : "trash";
          this.claim_target = tg_tile;

          let commands = res.commands_available;
          let skippable = true;
          for (let v of commands) {
            if (v.type == "ron") {
              skippable = false;
              break;
            }
          }
          this.players[this.player_id].commands_available = [
            { type: "skip" }
          ].concat(commands);
          this.players[this.player_id].allow_discard = false;

          if (res.agari_info != null) {
            this.yakulist = res.agari_info[1];
            this.calculated_score = res.agari_info[0];
          }
          let input_res;
          var cancelObj = { cancel: false };
          if (this.$store.state.skip_claim && skippable) {
            input_res = { type: "skip" };
          } else {
            let timeout = res.timeout * 1000;
            this.play_sound("sound1");
            input_res = await Promise.race([
              this.claim_input(cancelObj),
              this.timer(timeout, cancelObj)
            ]);
          }
          this.players[this.player_id].commands_available = [];
          this.players[this.player_id].allow_discard = false;
          this.yakulist = null;
          this.calculated_score = null;
          cancelObj.cancel = true;
          if (input_res != null) {
            input_res._m_id = res._m_id;
            this.conn.next(input_res);
          }
          this.players[tg_pl].target = null;
        } else if (res.type === "expose") {
          this.players[res.pid].exposed.push(res.obj);
          if( res.obj.discard_pos != null ){ 
            let [d_pid,d_pos] = res.obj.discard_pos
            this.players[d_pid].trash[d_pos].claimed = true
          }
        } else if (res.type === "apkong") {
          var ex = this.players[res.pid].exposed;
          for (var v of ex) {
            if (v.type == "pong" && v.tiles[0] == res.tile) {
              v.tiles.push(res.tile);
              v.type = "apkong";
              break;
            }
          }
        } else if (res.type == "confirm") {
          await new Promise(resolve => (this.listener_ok = resolve));
          this.conn.next({ _m_id: res._m_id });
          this.result = null;
        } else if (res.type == "discard") {
          await this.play_sound("sound2");
          this.players[res.pid].trash.push(res.tile);
        } else if (res.type == "your_turn") {
          // {"hand_tiles": [2, 4, 5, 6, 19, 22, 24, 34, 34, 38, 49, 52, 53], "draw": 22, "turn_commands_available": null, "_m_id": 4, "timeout": 1539603590.1542008}
          this.players[this.player_id].hand = res.hand_tiles;
          this.players[this.player_id].drawed = res.draw;
          this.players[this.player_id].commands_available =
            res.turn_commands_available == null
              ? []
              : res.turn_commands_available;
          this.players[this.player_id].allow_discard = true;
          if (res.agari_info != null) {
            this.yakulist = res.agari_info[1];
            this.calculated_score = res.agari_info[0];
          }
          var timeout = res.timeout * 1000;
          var cancelObj = { cancel: false };
          this.play_sound("sound1");
          var input_res = await Promise.race([
            this.turn_input(cancelObj),
            this.timer(timeout, cancelObj)
          ]);
          cancelObj.cancel = true;
          if (input_res != null) {
            input_res._m_id = res._m_id;
            this.conn.next(input_res);
          } else {
            pl.trash_tile(-1);
          }

          // await turn_input(this.player_id);
        }
      };
      this.conn.subscribe(proc)
    }

  },
  beforeRouteEnter(route, redirect, next) {
    next(vm => {
      if (window.socket == null) {
        vm.$router.push("/room");
        return false;
      }
    });
  }
};
</script>

<style scoped>
.clearfix:after {
  content: "";
  clear: both;
  display: block;
}

.player-field {
  width: 80%;
  height: 35%;
  box-sizing: border-box;
  /*  border: 2px blue solid;*/
}

#hand0 {
  position: absolute;
  left: 10%;
  top: 65%;
}

#hand1 {
  position: absolute;
  left: 42.5%;
  top: 32.5%;
  transform: rotate(-90deg);
}

#hand2 {
  position: absolute;
  left: 10%;
  top: 0%;
  transform: rotate(180deg);
}

#hand3 {
  position: absolute;
  left: -22.5%;
  top: 32.5%;
  transform: rotate(90deg);
}

#info {
  position: absolute;
  left: 35%;
  top: 35%;
  width: 30%;
  height: 30%;
  margin: auto;
  border: 1px orange solid;
}

#sideinfo {
  position: relative;
  width: 180px;
  height: 380px;
  padding: 5px;
  background: lightyellow;
  border: 1px orange solid;
  float: left;
}

.sideinfo-enter-active {
  animation-name: stretch-in;
  animation-timing-function: ease-in;
  animation-duration: 0.4s;
}
.sideinfo-leave-active {
  animation-name: stretch-in;
  animation-direction: reverse;
  animation-timing-function: ease-out;
  animation-duration: 0.4s;
}

@keyframes stretch-in {
  0% {
    transform: scaleX(0);
    transform-origin: 0 0;
  }
  100% {
    transform: scaleX(1);
    transform-origin: 0 0;
  }
}

.board-root {
  position: relative;
  background: rgb(231, 255, 231);
  width: 520px;
  height: 520px;
  margin-right: 0px;
  border: red solid 1px;
  float: left;
}
.jong-root {
  position: relative;
  margin: 0px auto;
  padding: 25px;
  width: 800px;
  height: 600px;
  display: inline-block;
}

body {
  margin: auto;
  overflow: hidden;
  font-size: 13px;
}
</style>
