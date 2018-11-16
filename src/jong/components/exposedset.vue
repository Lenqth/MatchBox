<template>
  <div class="exposed-group">
    <div v-if="type==='pong' || type==='chow' || type==='minkong'" v-for="(item,jndex) in tiles" class="exposed-item tile">
      <img v-bind:src="numtosrc(item)" >
    </div>
    <div v-if=" type==='apkong' " class="apkong-box">
      <div v-for="(item,jndex) in tiles.slice(0,3)">
        <div v-if="jndex === 1" class="kasane-container">
          <div class="kasane">
            <img v-bind:src="numtosrc(tiles[3])" class="tile-yoko" >
          </div>
          <div class="kasane">
            <img v-bind:src="numtosrc(item)" class="tile-yoko" >
          </div>
        </div>
        <span v-else>
          <img v-bind:src="numtosrc(item)" >
        </span>
        <spinning-target v-if="target && ( index + 1 == exposed.length )"></spinning-target>
      </div>
    </div>
    <div v-if=" type==='conckong' " v-for="(item,jndex) in tiles" class="exposed-item tile">
        <span v-if="jndex === 1">
          <img v-bind:src="numtosrc(item)" >
        </span>
        <span v-else>
          <img v-bind:src="numtosrc(0)">
        </span>
    </div>
  </div>
</template>
<script>
import Vue from 'vue';
import spinningtarget from './target.vue'
Vue.component('spinning-target',spinningtarget);

export default {
  props : {"tiles":{default: x=>[] },"type":{default:"chow"},"target":{default:false}},
}

</script>
<style>
</style>