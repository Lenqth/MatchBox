<template>
  <div class="my-discarded">
    <tile
      v-for="(item,index) in trash"
      class="discarded-item"
      :id="item.id"
      :yoko="item.yoko"
      :tsumogiri="item.tsumogiri"
      :claimed="item.claimed"
      :targeted="target && ( index + 1 == trash.length )"
      :key="index"
    />
  </div>
</template>
<script>
import Vue from "vue";

export default {
  props: ["trash", "target"],
  methods: {}
};
</script>
<style scoped>
.my-discarded {
  height: 40%;
  width: 37.5%;
  margin: auto;
}
.discarded-item {
  float: left;
  display: block;
  position: relative;
  margin: 1px;
  zoom: 0.8;
}
</style>
