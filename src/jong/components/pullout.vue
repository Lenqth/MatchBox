<template>
  <div class="pullout-area">
    <div v-if="pullout.length>=0" class="pullout-item tile">
      <img v-bind:src="numtosrc(65)" class="flower-tile">
      ×{{ pullout.length }}
    </div>
  </div>
</template>
<script>
import Vue from "vue";
import spinningtarget from "./target.vue";
import { get_wind_name, numtosrc } from "./jong_network.js";
Vue.component("spinning-target", spinningtarget);
export default {
  props: ["pullout", "target"],
  methods: {
    numtosrc,
    get_wind_name: get_wind_name
  }
};
</script>
<style>
.pullout-item {
  float: left;
}
.pullout-area {
  margin-right: auto;
  float: left;
  flex-basis: 10%;
  height: 33px;
  border: 1px pink dotted;
}
.flower-tile {
  zoom: 0.8;
}
</style>
