<template>

<div id="board-root" class="clearfix">
  <div id="info">
    <p>ノコリ：{{ deck_left }}</p>
    <p> {{  get_wind_name( prev_wind )  }}場 {{  get_wind_name(seat_wind)  }}風 </p>
    <p v-if="time_left!=null">入力待機 残り：{{  time_left.toFixed(1)  }}秒</p>
    <p>{{  message  }}</p>
  </div>
  <player-area id="hand1" v-bind:player="players[1]" class="player-field"></player-area>
  <player-area id="hand2" v-bind:player="players[2]" class="player-field"></player-area>
  <player-area id="hand3" v-bind:player="players[3]" class="player-field"></player-area>
  <player-area id="hand0" v-bind:player="players[0]" main=1 class="player-field"></player-area>
  <div id="sideinfo">
    <table>
      <tr v-for="(y,i) in yakulist">
        <td>{{ y.title }}</td>
        <td>{{ y.score }}</td>
      </tr>
    </table>
    <p style="">計 : {{ calculated_score }}</p>
  </div>
	<meld-selection v-bind:meld-selection="meld_selection"></meld-selection>
</div>

</template>

<script>
import Vue from 'vue';
import {Deck,get_wind_name,numtosrc} from './components/jong_network.js';
import * as utils from './components/utils.js' ;
var deck = new Deck();

function __img(x){ return '<img src="'+numtosrc(x)+'" >';}

import PlayerArea from './components/player.vue'
Vue.component('player-area',PlayerArea);

import meld_selection from './components/meld_selection.vue'
Vue.component('meld-selection',meld_selection);

window.deck = deck;

export default {
  name: 'Loader',
  data(){
    return deck;    
  },
  methods:{
    numtosrc,
    get_wind_name : get_wind_name
  }
}
</script>

<style>

.clearfix:after{
	content: "";
	clear: both;
	display: block;
}

.player-field{
  width:400px;
  height:200px;
  /* border: 2px blue solid; */
}

#hand0{
  position:absolute;
  left:100px;
  top:400px;
}

#hand1{
  position:absolute;
  left:300px;
  top:200px;
  transform:rotate(-90deg);
}

#hand2{
  position:absolute;
  left:100px;
  top:0px;
  transform:rotate(180deg);
}

#hand3{
  position:absolute;
  left:-100px;
  top:200px;
  transform:rotate(90deg);
}

#info{
  position:absolute;
  left:232px;
  top:232px;
  width:133px;
  height:133px;
  margin:auto;
  border: 1px orange solid;
}

#sideinfo{
  position:absolute;
  left:650px;
  top:50px;
  width:200px;
  height:400px;
  margin:auto;
  padding:15px;
  border: 1px orange solid;
}
#board-root{
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
	width: 600px;
	height: 600px;
	margin:auto;
	border: red solid 1px;
  position:absolute;
  display:inline-block;
}
body{
  margin:auto;
  overflow: hidden;
  font-size: 13px;
}


</style>
