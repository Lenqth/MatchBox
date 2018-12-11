<template>
  <transition-group name="command" class="root">
    <div key="open" v-if="open">
      <img :src="source" :width="width" :height="height" :alt="alt" class="card open">
    </div>
    <div key="close" v-else>
      <img :src="id2source(0)" :width="width" :height="height" :alt="id2alt(0)" class="card close">
    </div>
  </transition-group>
</template>
<script scoped>
import Vue from "vue";

const alt_table = [
  "z01",
  "s01",
  "s02",
  "s03",
  "s04",
  "s05",
  "s06",
  "s07",
  "s08",
  "s09",
  "s10",
  "s11",
  "s12",
  "s13",
  "",
  "h01",
  "h02",
  "h03",
  "h04",
  "h05",
  "h06",
  "h07",
  "h08",
  "h09",
  "h10",
  "h11",
  "h12",
  "h13",
  "",
  "d01",
  "d02",
  "d03",
  "d04",
  "d05",
  "d06",
  "d07",
  "d08",
  "d09",
  "d10",
  "d11",
  "d12",
  "d13",
  "",
  "c01",
  "c02",
  "c03",
  "c04",
  "c05",
  "c06",
  "c07",
  "c08",
  "c09",
  "c10",
  "c11",
  "c12",
  "c13",
  "x01",
  "x02"
];

const src_table = alt_table.map(x =>
  x != "" ? require("@/destiny7/assets/png/" + x + ".png") : null
);

export default {
  props: {
    card_id: {
      default: 0
    },
    open: { default: true },
    width: { default: 50 },
    height: { default: 75 }
  },
  methods: {
    id2source(id) {
      return src_table[id];
    },
    id2alt(id) {
      return alt_table[id];
    }
  },
  computed: {
    alt() {
      return this.id2alt(this.card_id);
    },
    source() {
      return this.id2source(this.card_id);
    }
  }
};
</script>
<style scoped>
.card {
  position: relative;
}

.open {
  border: 2px solid blue;
}
.close {
  border: 2px solid red;
}

.command-enter-active {
  transform: rotateY(90deg);
  animation-name: spin-in;
  animation-duration: 0.5s;
  animation-delay: 0.5s;
  z-index: 2;
  backface-visibility: hidden;
}
.command-leave-active {
  animation: spin-out;
  animation-duration: 0.5s;
  z-index: 1;
  backface-visibility: hidden;
}

@keyframes spin-out {
  0% {
    transform: rotateY(0deg);
  }
  100% {
    transform: rotateY(90deg);
  }
}
@keyframes spin-in {
  0% {
    transform: rotateY(90deg);
  }
  100% {
    transform: rotateY(0deg);
  }
}

.root {
  position: relative;
}
</style>