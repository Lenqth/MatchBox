<template>
  <v-dialog v-model="show" width="30vw" @close="fire_ok()">
    <v-card v-if="show" key="guard," style="overflow-x:hidden" > 
      <v-card-title font-large v-if="value.player != -1" class="headline">
        {{value.player}} の {{ value.tsumo ? "ツモ" : "ロン" }}
      </v-card-title>
      <v-card-title large v-else class="headline">
        流局
      </v-card-title>    
      <v-card-text>
        <yakulist :yakus="value.yaku" key='result-yaku' />
      </v-card-text>
      <v-card-actions>
        <span class="headline">計 {{value.score}} 点</span>
        <v-spacer/>
        <v-btn justify-right small @click="close">OK</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>

import Vue from 'vue' 
import {get_wind_name, numtosrc} from '../components/jong_network.js'

export default {
  props: {
    "value":{
      default:null
    },
  },
  methods: {
    numtosrc,
    get_wind_name: get_wind_name,
		fire_ok(){
			this.$emit("ok","");
    },
    close(){
      this.show=false;
    }
  },
  computed:{
    show:{
      get(){
        return (this.value != null)
      },
      set(v){
        if(!v){
          this.$emit("input",null)
          this.fire_ok();
        }
      }
    }
  },
}

</script>
<style scoped>

.result-top{
	font-size:20px;
}

.meld-select-enter-active{
  transition: top 0.6s 0s ease;
}
.meld-select-leave-active{
  transition: top 0.6s 0s ease;
}

.meld-select-enter , .meld-select-leave-to{
  top: 500px !important;
  display:none;
}

.score-box{
	font-size:20px;
	position:absolute;
	bottom : 40px;
	right: 40px;

}

</style>
