<template>
  <div
    class="tile"
    v-bind:class="{ 'tile-yoko': yoko , tsumogiri , claimed }"
    @mouseenter="onEnter"
    @mouseleave="onLeave"
  >
    <div v-if="highlighted" class="mini-marker"/>
    <img v-bind:src="numtosrc(id)">
    <spinning-target v-if="targeted"/>
  </div>
</template>
<script>
import Vue from "vue";
import spinningtarget from "./target.vue";
Vue.component("spinning-target", spinningtarget);

import { numtosrc } from "./jong_network.js";
export default {
  props: {
    id: {
      type: Number,
      default: 40
    },
    yoko: {
      type: Boolean,
      default: false
    },
    tsumogiri: {
      type: Boolean,
      default: false
    },
    claimed: {
      type: Boolean,
      default: false
    },
    targeted: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    numtosrc,
    onEnter(e) {
      this.$store.commit("hover_tile", this.id);
    },
    onLeave(e) {
      this.$store.commit("hover_tile", null);
    }
  },
  computed: {
    highlighted() {
      return this.$store.state.hover_tile_id == this.id;
    }
  }
};
</script>
<style scoped>
.tile-yoko {
  display: block;
  transform-origin: top left;
  transform: rotate(-90deg) translate(-100%);
  margin-bottom: -50%;
  white-space: nowrap;
}
.mini-marker {
  background-color: blue;
  position: absolute;
  width: 10px;
  height: 4px;
  z-index: 1;
}
.tile.tsumogiri {
  outline: 1px blue solid;
}

.claimed img {
  filter: brightness(0.6);
}
img {
  display: block;
}
</style>