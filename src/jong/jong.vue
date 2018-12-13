<template>
  <div class="jong-root">
    <div id="board-root" class="board-root">
      <div id="info">
        <p>ノコリ：{{ deck_left }}</p>
        <p>{{ get_wind_name( prev_wind ) }}場 {{ get_wind_name(seat_wind) }}風</p>
        <p v-if="time_left!=null">入力待機 残り：{{ time_left.toFixed(1) }}秒</p>
        <p>{{ message }}</p>
      </div>
      <player-area id="hand1" v-bind:player="players[(player_id+1)%4]" class="player-field"></player-area>
      <player-area id="hand2" v-bind:player="players[(player_id+2)%4]" class="player-field"></player-area>
      <player-area id="hand3" v-bind:player="players[(player_id+3)%4]" class="player-field"></player-area>
      <player-area id="hand0" v-bind:player="players[player_id]" main="1" class="player-field"></player-area>
      <meld-selection v-bind:meld_selection="meld_selection" v-on:cancel="meld_selection_cancel()"></meld-selection>
      <result-dialog v-bind:result="result" v-on:ok="ok()"></result-dialog>
      <final-result-dialog v-bind:result="final_result" v-on:ok="ok()"></final-result-dialog>
    </div>
    <div id="sideinfo">
      <table>
        <tr v-for="(y,i) in yakulist" :key="i">
          <td>{{ y.title }}</td>
          <td>{{ y.score }}</td>
        </tr>
      </table>
      <p style>計 : {{ calculated_score }}</p>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import { Deck, get_wind_name, numtosrc } from "./components/jong_network.js";
import * as utils from "./components/utils.js";

import PlayerArea from "./components/player.vue";
Vue.component("player-area", PlayerArea);

import Result from "./components/result.vue";
Vue.component("result-dialog", Result);

import FinalResult from "./components/final_result.vue";
Vue.component("final-result-dialog", FinalResult);

import meld_selection from "./components/meld_selection.vue";
Vue.component("meld-selection", meld_selection);

var deck = new Deck();

function __img(x) {
  return '<img src="' + numtosrc(x) + '" >';
}

window.deck = deck;

export default {
  name: "Loader",
  data() {
    return deck;
  },
  methods: {
    numtosrc,
    get_wind_name: get_wind_name,
    ok() {
      deck.ok();
    },
    meld_selection_cancel() {
      deck.meld_selection = null;
    }
  },
  beforeRouteEnter(route, redirect, next) {
    next(vm => {
      if (window.socket == null) {
        vm.$router.push("/room");
      } else {
        deck.start(window.socket);
      }
    });
  }
};
</script>

<style>
.clearfix:after {
  content: "";
  clear: both;
  display: block;
}

.player-field {
  width: 400px;
  height: 200px;
  /* border: 2px blue solid; */
}

#hand0 {
  position: absolute;
  left: 100px;
  top: 400px;
}

#hand1 {
  position: absolute;
  left: 300px;
  top: 200px;
  transform: rotate(-90deg);
}

#hand2 {
  position: absolute;
  left: 100px;
  top: 0px;
  transform: rotate(180deg);
}

#hand3 {
  position: absolute;
  left: -100px;
  top: 200px;
  transform: rotate(90deg);
}

#info {
  position: absolute;
  left: 232px;
  top: 232px;
  width: 133px;
  height: 133px;
  margin: auto;
  border: 1px orange solid;
}

#sideinfo {
  position: absolute;
  margin: 50px;
  left: 600px;
  top: 100px;
  width: 160px;
  height: 380px;
  padding: 10px;
  border: 1px orange solid;
}

.board-root {
  position: relative;
  margin: 50px;
  width: 600px;
  height: 600px;
  border: red solid 1px;
}
.jong-root {
  position: relative;
  margin: 50px;
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
