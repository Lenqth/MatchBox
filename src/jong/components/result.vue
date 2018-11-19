<template>
  <div v-if="result!=null" class="result-box">
    <div class="result-top">
      {{result.player}} の {{ result.type }}
    </div>
    <div class="yaku-group">
			役：
      <div v-for="(item,index) in result.yaku">
				{{item}}
      </div>
    </div>
    <div class="score-box">
      計 {{result.score}} 点
    </div>
  </div>
</template>
<script>

import Vue from 'vue';
import {get_wind_name,numtosrc} from '../components/jong_network.js';

export default {
  props : ["result"]  ,
  methods:{
    numtosrc,
    get_wind_name : get_wind_name
  },
}
  
</script>
<style>

.result-box{
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
	margin:auto;
  padding:8px;
}

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