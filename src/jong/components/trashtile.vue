<template>
  <div class="my-discarded">
    <div v-for="(item,index) in trash" class="discarded-item tile" v-bind:class="{ 'tile-yoko': item.yoko , 'discarded-tsumogiri' : item.tsumogiri , 'claimed' : item.claimed }">
      <img v-bind:src="numtosrc(item.id)">
      <spinning-target v-if="target && ( index + 1 == trash.length )"></spinning-target>
    </div>
  </div>
</template>
<script>
import Vue from 'vue'
import {get_wind_name, numtosrc} from './jong_network.js'

import spinningtarget from './target.vue'
Vue.component('spinning-target', spinningtarget)
export default {
  props: ['trash', 'target'],
  methods: {
    numtosrc,
    get_wind_name: get_wind_name
  }
}
</script>
<style scoped>

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
  position: relative;
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
 
.claimed>img {
  filter: brightness(0.6);
}

</style>
