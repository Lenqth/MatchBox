<template>
  <v-card>
    <result-dialog v-model="result" @ok="ok"/>
    <v-btn @click="clk">RESULT</v-btn>
    <v-btn @click="testrx">TESTRX</v-btn>
  </v-card>
</template>
<script>

import Vue from 'vue';

import Yakulist from "@/jong/components/yakulist.vue";
import Result from "@/jong/components/result.vue";
import FinalResult from "@/jong/components/final_result.vue";
Vue.component("yakulist", Yakulist);
Vue.component("result-dialog", Result);
Vue.component("final-result-dialog", FinalResult);

import rxconnection from "@/common/rxconnection.ts";



import {Observable,Observer,Subject} from "rxjs";
import {  share, distinctUntilChanged, takeWhile, shareReplay } from 'rxjs/operators';

export default {
  data(){
    return {
      result : null
    }
  },
  methods:{
    ok(){
      console.log('ok')
    },
    testrx(){
      var q;
      var o = new Observable((observer) => {
          q = observer;
        }).pipe(
          shareReplay(1),
          distinctUntilChanged()
        );

      o.subscribe( (x) => console.log("1:"+x) );
      q.next(true);
      o.subscribe( (x) => console.log("2:"+x) );
      q.next(false);
      o.subscribe( (x) => console.log("3:"+x) );
      q.next(true);
    },
    clk(){
      var result = {player:"あああ",tsumo:true,yaku:[],score:10};
      result.yaku.push({"chinese_name":"てすと1","score":1})
      result.yaku.push({"chinese_name":"てすと2","score":2})
      result.yaku.push({"chinese_name":"てすと3","score":3})
      result.yaku.push({"chinese_name":"てすと4","score":4})
      this.result = result
    }
  }
}
  
</script>

<style scoped>


</style>