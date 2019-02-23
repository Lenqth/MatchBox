
<template>
  <div class="exposed-group">
    <div
      v-if="type==='pong' || type==='chow' || type==='minkong'"
      v-for="(item,jndex) in tiles"
      class="exposed-item tile"
      :key="jndex"
    >
      <tile :id="item"/>
    </div>
    <div v-if=" type==='apkong' " class="apkong-box">
      <div v-for="(item,jndex) in tiles.slice(0,3)" :key="jndex">
        <div v-if="jndex === 1" class="kasane-container">
          <div class="kasane">
            <tile :id="tiles[3]" :yoko="true"/>
          </div>
          <div class="kasane">
            <tile :id="item" :yoko="true"/>
          </div>
        </div>
        <span v-else>
          <tile :id="item"/>
        </span>
        <spinning-target v-if="target && ( index + 1 == exposed.length )"></spinning-target>
      </div>
    </div>
    <div
      v-if=" type==='conckong' "
      v-for="(item,jndex) in tiles"
      class="exposed-item tile"
      :key="jndex"
    >
      <span v-if="jndex === 1 && show_conc">
        <tile :id="item"/>
      </span>
      <span v-else>
        <tile :id="0"/>
      </span>
    </div>
  </div>
</template>
<script>
import Vue from "vue";
import spinningtarget from "./target.vue";
Vue.component("spinning-target", spinningtarget);

export default {
  props: {
    tiles: { default: x => [] },
    type: { default: "chow" },
    target: { default: false },
    show_conc: { default: false }
  },
  methods: {}
};
</script>
<style scoped>
.exposed-group {
  flex-wrap: nowrap;
  box-sizing: border-box;
  /*  border: 1px red dotted;*/
  display: flex;
  margin: 0px 4px;
}

.tile-yoko {
  display: block;
  transform-origin: top left;
  transform: rotate(-90deg) translate(-100%);
  margin-bottom: -50%;
  white-space: nowrap;
}

.kasane {
  height: 22px;
  width: 30px;
}
.kasane > img {
  float: left;
}
.apkong-box {
  align-items: flex-end;
  display: inline-flex;
}
</style>
