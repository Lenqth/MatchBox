<template>
  <div id="meld-select">
    <transition name="meld-select">
      <div v-if="meld_selection != null && meld_selection.tiles.length > 0" class="meld-select-box">
        <div v-for="(grp,index) in meld_selection.tiles" class="exposed-group group-clickable" v-on:click="click_meld_popup(index);">
          <div v-for="(item,jndex) in grp" class="exposed-item tile">
            <img v-bind:src="numtosrc(item)" >
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>
<script>

import Vue from 'vue'
import {get_wind_name, numtosrc, click_meld_popup} from './jong_network.js'

export default {
  props: ['meld_selection'],
  methods: {
    numtosrc,
    get_wind_name: get_wind_name,
    click_meld_popup: click_meld_popup
  }
}

</script>
<style>
.group-clickable:hover{
  background: orange;
}
.exposed-area{
	display: flex;
	flex-wrap: nowrap;
  margin-left: auto;
  width:75%;
  height:33px;
}
.tile{
	flex-wrap: nowrap;
  margin:1px;
  position:relative;
}

.exposed-group{
	flex-wrap: nowrap;
  margin-left: 5px;
  border: 1px red dotted;
  display: flex;
}

.meld-select-box{
  border: solid 2px orange;
  background: lightgray;
  opacity: 0.6;
  position: absolute;
  width: 400px;
  height: 250px;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
	margin:auto;
  padding:8px;
}

.meld-select-enter-active{
  transition: top 0.6s 0s ease;
}
.meld-select-leave-active{
  transition: top 0.6s 0s ease;
}

.meld-select-enter , .meld-select-leave-to{
  top: 500px !important;
  display:none;
}

</style>
