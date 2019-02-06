<template>
  <div>
    <trash-tile v-bind:trash="player.trash" v-bind:target="player.target=='trash'"></trash-tile>
		<div class="score-area">{{player.score}}</div>
    <command-bar v-show="main" :class="{'player-main':main}" :commands_available="player.commands_available" @command="command" />
    <table class="player-hand" :class='{"border-discard-hand":player.allow_discard,"player-main":(main||open)}'>
      <tr>
      <td v-for="(item,index) in player.hand" :key="index">
        <span v-on:click="tile_click(index)" >
            <img v-bind:src="numtosrc(item)" >
        </span>
      </td>
      <td width='10'></td>
      <td v-if="player.drawed != null" v-on:click="tile_click(-1);" >
        <img v-bind:src="numtosrc(player.drawed)" >
      </td>
      </tr>
    </table>
		<div class="bottom-bar">
			<pullout-tile v-bind:pullout="player.pullout"></pullout-tile>
	    <div class="exposed-area">
	        <exposed-set v-for="(grp,index) in player.exposed" v-bind:type="grp.type" v-bind:tiles="grp.tiles"
          v-bind:target="player.target=='apkong'" v-bind:show_conc="(main || open)" :key="index"></exposed-set>
	    </div>
		</div>
  </div>
</template>
<script>
import Vue from 'vue'
import exposedset from './exposedset.vue'
import pullout from './pullout.vue'
import trashtile from './trashtile.vue'
import spinningtarget from './target.vue'
import command_bar from './command_bar.vue'

import {get_wind_name, numtosrc, tile_click, command, click_meld_popup} from './jong_network.js'
Vue.component('exposed-set', exposedset)
Vue.component('pullout-tile', pullout)
Vue.component('trash-tile', trashtile)
Vue.component('spinning-target', spinningtarget)
Vue.component('command-bar', command_bar)

export default {
  props: [ 'player', 'main' , 'open' ],
  methods: {
    numtosrc,
    get_wind_name: get_wind_name,
    tile_click(x){
      this.$emit("tile",x)
    },
    command(x,y){
      this.$emit("command",x,y)
    }
  }
}
</script>
<style scoped>

@keyframes up {
  0% {top: 1500px;display:none;opacity:0;}
  0.1% {top: 1500px;opacity:0;}
  100% {display:block;}
}
@keyframes down {
  0% {display:block;}
  99.9% {top: 1500px;opacity:0;}
  100% {top: 1500px;opacity:0;display:none;}
}
.anim-show {
    height: 14px;
    transition-property: height;
    transition-duration: 0.6s;
    transition-delay: 0s;
    transition-timing-function: ease;
}

.border-discard-hand{
	outline:1px orange solid;
	animation: blinkborder 0.7s ease 0.4s infinite alternate;
}


.bottom-bar{
	width:110%;
	display: flex;
	flex-wrap:nowrap;
}
.exposed-area{
	display: flex;
	flex-wrap: nowrap;
  margin-left: auto;
  flex-basis:75%;
  height:33px;
}
.score-area{
  position:absolute;
  left:70%;
  top:5%;
  width: 10%;
	line-height:33px;
	border: 1px blue dotted;
	text-align: right;
	vertical-align: middle;
	padding-right: 5px;
	font-size: 16px;
}
.player-hand:not(.player-main){
  visibility: hidden;
}

</style>
