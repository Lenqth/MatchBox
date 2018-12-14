<template>
  <table class="board-root">
      <tr v-for=" (row,jndex) in board " :key="jndex" >
      <td v-for=" (item,index) in row " class="board-cell" :key="index">
          <div v-if="item<16" class="piece" v-bind:class="item2class(item)" ></div>
      </td>
      </tr>
  </table>
</template>
<script>

import Vue from 'vue';

import {item2class} from './quarto'

export default {
  props:["board"],
  methods : {
      item2class
      
  }  
}
  
</script>
<style scoped>
.circle{
  border-radius: 50%;
}
.square{
  border-radius: 10%;
}
.big{
  border-width : 14px !important ;
  width:48px;
  height:48px;
}
.small{
  width:24px;
  height:24px;
}
.hole.black{
  border: #110000 7px solid;
  background:transparent;
}
.hole.white{
  border: #ffffee 7px solid;
  background:transparent;
}
.nohole.black{
  background : #110000;
}
.nohole.white{
  background : #ffffee;
}
.piece{
  box-sizing: border-box;
  position:absolute;
  margin:auto;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;

}
.piece-cell{
  position:relative;
  width:50px;
  height:50px;
  background:lightgray;
  box-sizing: border-box;
  flex-basis:25%;
}
.board-root{
  margin : 5vh;
  border:1px black solid;
  box-sizing: border-box;
}
.board-cell{
  position:relative;
  width:50px;
  height:50px;
  background:lightgray;
  box-sizing: border-box;
}
</style>