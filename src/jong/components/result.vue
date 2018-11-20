<template>
  <div v-if="result!=null" class="result-box">
    <div class="result-top">
      {{result.player}} の {{ result.tsumo ? "ツモ" : "ロン" }}
    </div>
    <div class="yaku-group">
			<table class="yaku-table">
				<thead class="yaku-thead">
					<tr>
						<td class="row-yaku"> 役 </td>
						<td class="row-score"> 点 </td>
					</tr>
				</thead>
				<tbody class="yaku-tbody">
		      <tr v-for="(item,index) in result.yaku" :key="index">
						<td>{{item.chinese_name}}</td>
						<td>{{item.score}}</td>
		      </tr>
				</tbody>
			</table>
    </div>
    <div class="score-box">
      計 {{result.score}} 点
    </div>
  </div>
</template>
<script>

import Vue from 'vue'
import {get_wind_name, numtosrc} from '../components/jong_network.js'

export default {
  props: ['result'],
  methods: {
    numtosrc,
    get_wind_name: get_wind_name
  }
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

.yaku-table{
	width:80%;
	margin: auto;
}
.yaku-thead{
	background-color: pink;
}
.yaku-tbody{

}
.yaku-tbody>:nth-child(odd){
	background-color: lightgreen;
}
.yaku-tbody>:nth-child(even){
	background-color: lightblue;
}

.row-yaku{
	width:60%;
}
.row-score{
	width:20%;
}
</style>
