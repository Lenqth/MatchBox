<template>
  <v-dialog v-model="show" width="30vw">
    <v-card v-if="show">
      <v-card-text>
        <table class="ranking-table">
          <thead class="ranking-thead">
            <tr>
              <td>順位</td>
              <td class="row-yaku">名前</td>
              <td class="row-score">点数</td>
            </tr>
          </thead>
          <tbody class="ranking-tbody">
            <tr v-for="(item,index) in result" :key="index">
              <td>{{1+index}}</td>
              <td>{{item.name}}</td>
              <td>{{item.point}}</td>
            </tr>
          </tbody>
        </table>
      </v-card-text>
      <v-card-actions>
        <v-spacer/>
        <v-btn justify-right small @click="fire_ok()">OK</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import Vue from "vue";

export default {
  props: {
    result: {
      default: null
    }
  },
  data() {
    return { show: false };
  },
  methods: {
    fire_ok() {
      this.$emit("ok", "");
    }
  },
  watch: {
    result(v) {
      this.show = v != null;
    },
    show(v) {
      if (!v) {
        this.result = null;
        this.fire_ok();
      }
    }
  }
};
</script>
<style scoped>
.result-box {
  border: solid 2px orange;
  background: lightgray;
  opacity: 0.9;
  position: absolute;
  width: 300px;
  height: 400px;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  margin: auto;
  padding: 8px;
}

.result-top {
  font-size: 20px;
}

.score-box {
  font-size: 20px;
  position: absolute;
  bottom: 40px;
  right: 40px;
}

.ranking-table {
  width: 80%;
  margin: auto;
}
.ranking-thead {
  background-color: pink;
}
.ranking-tbody {
}
.ranking-tbody > :nth-child(1) {
  background-color: gold;
  height: 2em;
}
.ranking-tbody > :nth-child(2) {
  background-color: silver;
  height: 1.8em;
}
.ranking-tbody > :nth-child(3) {
  background-color: burlywood;
  height: 1.6em;
}
.ranking-tbody > :nth-child(2n + 5) {
  background-color: lightgreen;
}
.ranking-tbody > :nth-child(2n + 4) {
  background-color: lightblue;
}

.row-yaku {
  width: 60%;
}
.row-score {
  width: 20%;
}
</style>
