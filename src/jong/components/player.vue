<template>  
  <div>
    <trash-tile v-bind:trash="player.trash" v-bind:target="player.target=='trash'"></trash-tile>
    <div v-if="main" class="command-bar clearfix" style="width:100%;height:24px;">
      <transition-group class="command-bar clearfix" name="command">
        <div id="chow" key="chow" v-if="player.command_types_available.has('chow')" class="command" onclick="command('chow');">チー(Z)</div>
        <div id="pong" key="pong" v-if="player.command_types_available.has('pong')" class="command" onclick="command('pong');">ポン(X)</div>
        <div id="kong" key="kong" v-if="player.command_types_available.has('kong')" class="command" onclick="command('kong');">カン(C)</div>
        <div id="conckong" key="conckong" v-if="player.command_types_available.has('conckong')" class="command" onclick="command('conckong');">暗カン</div>
        <div id="apkong" key="apkong" v-if="player.command_types_available.has('apkong')" class="command" onclick="command('apkong');">加カン</div>
        <div id="ron" key="ron" v-if="player.command_types_available.has('ron')" class="command" onclick="command('ron');">ロン</div>
        <div id="tsumo" key="tsumo" v-if="player.command_types_available.has('tsumo')" class="command" onclick="command('tsumo');">ツモ</div>
        <div id="skip" key="skip" v-if="player.command_types_available.has('skip')" class="command" onclick="command('skip');">スキップ</div>
      </transition-group>
    </div>
    <table v-bind:class="{'border-discard-hand':player.allow_discard}">
      <tr>
      <td v-for="(item,index) in player.hand">
        <span v-bind:pos="index" onClick="tile_click(this);" >
            <img v-bind:src="numtosrc(item)" >
        </span>
      </td>
      <td width='20'></td>
      <td v-if="player.drawed != null" pos="-1" onClick="tile_click(this);" >
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
import Vue from 'vue';
import exposedset from './exposedset.vue'
Vue.component('exposed-set',exposedset);
import pullout from './pullout.vue'
Vue.component('pullout-tile',exposedset);
import trashtile from './trashtile.vue'
Vue.component('trash-tile',trashtile);
import spinningtarget from './target.vue'
Vue.component('spinning-target',spinningtarget);



export default {
  props : ["player","main"]
}
</script>
<style>

</style>
