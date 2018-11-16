<template>
  <div id="meld-select">
    <transition name="meld-select">
      <div v-if="meld_selection != null && meld_selection.tiles.length > 0" class="meld-select-box">
        <div v-for="(grp,index) in meld_selection.tiles" class="exposed-group group-clickable" v-bind:pos="index" onclick="click_meld_popup(this.getAttribute('pos'));">
          <div v-for="(item,jndex) in grp" class="exposed-item tile">
            <img v-bind:src="numtosrc(item)" >
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>
<script>

import Vue from 'vue';

export default {
  props : ["meld_selection"]  
}
  
</script>
<style>

</style>