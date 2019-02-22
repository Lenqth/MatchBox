<template>
  <v-card>
    <result-dialog v-model="result" @ok="ok"/>
    <v-btn @click="clk">RESULT</v-btn>
    <v-btn @click="testrx">TESTRX</v-btn>
    <div style="display:flex;flex-wrap: nowrap;margin:auto;width:200px;">
      <tile :id="40"/>
      <tile :id="40"/>
      <tile :id="41"/>
      <tile :id="41"/>
    </div>
  </v-card>
</template>
<script>
import Vue from "vue";

import Yakulist from "@/jong/components/yakulist.vue";
import Result from "@/jong/components/result.vue";
import FinalResult from "@/jong/components/final_result.vue";
Vue.component("yakulist", Yakulist);
Vue.component("result-dialog", Result);
import Tile from "@/jong/components/tile.vue";
Vue.component("tile", Tile);
Vue.component("final-result-dialog", FinalResult);

import rxconnection from "@/common/rxconnection.ts";

import { Observable, Observer, Subject, timer, defer } from "rxjs";
import * as operators from "rxjs/operators";

export default {
  data() {
    return {
      result: null,
      count: 0,
      observer: null
    };
  },
  methods: {
    ok() {
      console.log("ok");
    },
    sender() {
      this.observer.next(1 + this.count);
      this.observer.next(2 + this.count);
      if (this.count++ >= 5) {
        this.observer.complete();
        return;
      }
      this.observer.error("q");
    },
    testrx() {
      var o = new Observable(observer => {
        this.observer = observer;
      }).pipe(
        operators.retryWhen(x =>
          x.pipe(
            operators.mergeMap((e, i) => {
              console.log(i + " error");
              return timer(i * 500).pipe(
                operators.flatMap(async x => {
                  await this.sender();
                  return x;
                })
              );
            })
          )
        )
      );
      var sleep = t => new Promise(r => setTimeout(r, t));
      o.subscribe(
        x => console.log("1:" + x),
        e => {
          console.log("1e:" + e);
        }
      );
      this.sender();
    },
    clk() {
      var result = { player: "あああ", tsumo: true, yaku: [], score: 10 };
      result.yaku.push({ chinese_name: "てすと1", score: 1 });
      result.yaku.push({ chinese_name: "てすと2", score: 2 });
      result.yaku.push({ chinese_name: "てすと3", score: 3 });
      result.yaku.push({ chinese_name: "てすと4", score: 4 });
      this.result = result;
    }
  }
};
</script>

<style scoped>
</style>