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
import {get_wind_name,numtosrc} from './jong_network.js';
import spinningtarget from './target.vue'
Vue.component('spinning-target',spinningtarget);

export default {
  props : {"tiles":{default: x=>[] },"type":{default:"chow"},"target":{default:false}},
  methods:{
    numtosrc,
    get_wind_name : get_wind_name
  },
}

</script>
<style>


.tile-yoko{
  display: block;
  transform-origin: top left;
  transform: rotate(-90deg) translate(-100%);
  margin-bottom: -50%;
  white-space: nowrap;
}

.kasane{
  height: 22px;
  width: 30px;
}
.kasane > img {
  float:left;
}
.apkong-box{
  align-items:flex-end;
  display: inline-flex;
}

.my-discarded{
  height:100px;
  width:210px;
  margin:auto;
}
.discarded-item{
  float: left;
  display: block;
}
.discarded-item img {
  width:22px;
  height:30px;
  display: block;
  border: 1px transparent solid;
}

.discarded-tsumogiri img{
  border: 1px blue solid;
}
.pullout-item{
  float: left;
}
.exposed-item{
  float: left;
  direction: rtl;
}
.pullout-area{
  margin-right: auto;
  float: left;
  width:20%;
  height:33px;
  border: 1px pink dotted;
}
.exposed-area{
	display: flex;
	flex-wrap: nowrap;
  margin-left: auto;
  width:75%;
  height:33px;
}
</style>