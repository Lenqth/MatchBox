<template>

<div id="board-root" class="clearfix">
  <div id="info">
    <p>ノコリ：$${ deck_left }</p>
    <p> $${ get_wind_name( prev_wind ) }場 $${ get_wind_name(seat_wind) }風 </p>
    <p v-if="time_left!=null">入力待機 残り：$${ time_left.toFixed(1) }秒</p>
    <p>$${ message }</p>
  </div>
  <player-area id="hand1" v-bind:player="players[1]" class="player-field"></player-area>
  <player-area id="hand2" v-bind:player="players[2]" class="player-field"></player-area>
  <player-area id="hand3" v-bind:player="players[3]" class="player-field"></player-area>
  <player-area id="hand0" v-bind:player="players[0]" main=1 class="player-field"></player-area>
  <div id="sideinfo">
    <table>
      <tr v-for="(y,i) in yakulist">
        <td>$${y.title}</td>
        <td>$${y.score}</td>
      </tr>
    </table>
    <p style="">計 : $${calculated_score}</p>
  </div>
  <div id="meld-select">
    <transition name="meld-select">
      <div v-if="meld_selection.meld_selection.length > 0" class="meld-select-box">
        <div v-for="(grp,index) in meld_selection.meld_selection" class="exposed-group group-clickable" v-bind:pos="index" onclick="click_meld_popup(this.getAttribute('pos'));">
          <div v-for="(item,jndex) in grp" class="exposed-item tile">
            <img v-bind:src="numtosrc(item)" >
          </div>
        </div>
      </div>
    </transition>
  </div>
</div>

</template>

<script>
import PlayerArea from './components/player.vue'
Vue.component('player-area',PlayerArea);

export default {
  name: 'App'
}
</script>

<style>

</style>
