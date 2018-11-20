<template>
  <div>
    <trash-tile v-bind:trash="player.trash" v-bind:target="player.target=='trash'"></trash-tile>
    <div v-if="main" class="command-bar clearfix" style="width:100%;height:24px;">
      <transition-group class="command-bar clearfix" name="command">
        <div id="chow" key="chow" v-if="player.command_types_available.has('chow')" class="command" v-on:click="command('chow');">チー(Z)</div>
        <div id="pong" key="pong" v-if="player.command_types_available.has('pong')" class="command" v-on:click="command('pong');">ポン(X)</div>
        <div id="kong" key="kong" v-if="player.command_types_available.has('kong')" class="command" v-on:click="command('kong');">カン(C)</div>
        <div id="conckong" key="conckong" v-if="player.command_types_available.has('conckong')" class="command" v-on:click="command('conckong');">暗カン</div>
        <div id="apkong" key="apkong" v-if="player.command_types_available.has('apkong')" class="command" v-on:click="command('apkong');">加カン</div>
        <div id="ron" key="ron" v-if="player.command_types_available.has('ron')" class="command" v-on:click="command('ron');">ロン</div>
        <div id="tsumo" key="tsumo" v-if="player.command_types_available.has('tsumo')" class="command" v-on:click="command('tsumo');">ツモ</div>
        <div id="skip" key="skip" v-if="player.command_types_available.has('skip')" class="command" v-on:click="command('skip');">スキップ</div>
      </transition-group>
    </div>
    <table v-bind:class="{'border-discard-hand':player.allow_discard}">
      <tr>
      <td v-for="(item,index) in player.hand">
        <span v-on:click="tile_click(index);" >
            <img v-bind:src="numtosrc(item)" >
        </span>
      </td>
      <td width='20'></td>
      <td v-if="player.drawed != null" v-on:click="tile_click(-1);" >
        <img v-bind:src="numtosrc(player.drawed)" >
      </td>
      </tr>
    </table>
    <pullout-tile v-bind:pullout="player.pullout"></pullout-tile>
    <div class="exposed-area">
        <exposed-set v-for="(grp,index) in player.exposed" v-bind:type="grp.type" v-bind:tiles="grp.tiles" v-bind:target="player.target=='apkong'"></exposed-set>
    </div>
  </div>
</template>
<script>
import Vue from 'vue'
import exposedset from './exposedset.vue'
import pullout from './pullout.vue'
import trashtile from './trashtile.vue'
import spinningtarget from './target.vue'

import {get_wind_name, numtosrc, tile_click, command, click_meld_popup} from './jong_network.js'
Vue.component('exposed-set', exposedset)
Vue.component('pullout-tile', pullout)
Vue.component('trash-tile', trashtile)
Vue.component('spinning-target', spinningtarget)

export default {
  props: ['player', 'main'],
  methods: {
    numtosrc,
    get_wind_name: get_wind_name,
    tile_click,
    command
  }
}
</script>
<style>

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
.command-bar{
  display: flex;
  flex-wrap: nowrap;
}

.command{
  background-color: white;
  border:1px black solid;
  width:60px;
  font-size: 14px;
  height: 14px;
}
.command-enter-active{
  transition: height 0.6s 0s ease;
}
.command-leave-active{
  transition: height 0.6s 0s ease;
}

.command-enter , .command-leave-to{
  height: 0px;
}

.border-discard-hand{
	outline:1px orange solid;
	animation: blinkborder 0.7s ease 0.4s infinite alternate;
}

</style>
