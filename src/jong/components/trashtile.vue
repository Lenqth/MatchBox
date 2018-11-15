<template>
  <div class="my-discarded">
    <div v-for="(item,index) in trash" class="discarded-item tile" v-bind:class="{ 'tile-yoko': item.yoko , 'discarded-tsumogiri' : item.tsumogiri }">
      <img v-bind:src="numtosrc(item.id)">
      <spinning-target v-if="target && ( index + 1 == trash.length )"></spinning-target>
    </div>
  </div>
</template>
<script>

import spinningtarget from './target.vue'
Vue.component('spinning-target',spinningtarget);
export default {
  props : ["trash","target"],
}
</script>
<style>
</style>