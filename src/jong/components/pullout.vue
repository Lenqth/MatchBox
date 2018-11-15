<template>
  <div class="pullout-area">
    <div v-if="pullout.length>0" class="pullout-item tile">
        <img v-bind:src="numtosrc(65)" > × {{ pullout.length }}
    </div>
  </div>
</template>
<script>
import spinningtarget from './target.vue'
Vue.component('spinning-target',spinningtarget);
export default {
  props : ["pullout","target"]
}
</script>
<style>
</style>