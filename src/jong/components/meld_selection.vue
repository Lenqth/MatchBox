<template>
  <div>
    <transition name="meld-select">
      <div class="modal-mask" v-if="meld_selection != null && meld_selection.tiles.length > 0" v-on:click="close()">
        <div class="modal-wrapper">
          <div class="meld-select-box">
            <div v-for="(grp,index) in meld_selection.tiles" class="exposed-group group-clickable" v-on:click="click_meld_popup(index);" :key="index" >
              <div v-for="(item,jndex) in grp" class="exposed-item tile" :key="jndex">
                <img v-bind:src="numtosrc(item)" >
              </div>
            </div>
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
    click_meld_popup: click_meld_popup,
    close(){
      this.$emit("cancel")
    }    
  }
}

</script>
<style scoped>
.group-clickable:hover{
  background: orange;
}
.tile{
	flex-wrap: nowrap;
  margin:1px;
  position:relative;
}

.exposed-group{
	flex-wrap: nowrap;
  border: 1px red dotted;
  display: flex;
  margin:0px 4px;
}

.meld-select-box{
  border: solid 2px orange;
  background: lightgray;
  width: 400px;
  height: 250px;
  opacity: 0.8;
  display: flex;
  align-items : center;
  padding:8px;
  margin: 0px auto;
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


.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

</style>
