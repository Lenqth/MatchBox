<template>
  <div>
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
    <transition name="sideinfo">
      <div v-if="yakulist!=null" id="sideinfo">
        <yakulist :yakus="yakulist" />
        <p style>計 : {{ calculated_score }}</p>
      </div>
    </transition>
  </div>
  </div>
</template>

<script>
import Vue from "vue";
import { Deck, get_wind_name, numtosrc } from "./components/jong_network.js";
import * as utils from "./components/utils.js";

import PlayerArea from "./components/player.vue";
Vue.component("player-area", PlayerArea);

import Yakulist from "./components/yakulist.vue";
Vue.component("yakulist", Yakulist);

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
  width: 80% ;
  height: 35% ;
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
  top: 32.5% ;
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
  position:relative;
  width: 180px;
  height: 380px;
  padding: 5px;
  background: lightyellow;
  border: 1px orange solid; 
  float: left;  
}

.sideinfo-enter-active{
  animation-name: stretch-in;
	animation-timing-function: ease-in;
  animation-duration: 0.4s;
}
.sideinfo-leave-active{
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
  margin-right:0px;
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
