<template>
  <div id="board-root" class="clearfix">
    <board :board="board"/>
    <div id="leftpieces">
        <div v-for=" (item,index) in piece " class="piece-cell" :key="index" >
        <div v-if="item" class="piece" v-bind:class="item2class(index)"></div>
        </div>
    </div>
  </div>
</template>
<script>

import Vue from 'vue';
import {item2class} from './components/quarto'

var data = {};
data.board = (new Array(4).fill(0)).map( () => new Array(4).fill(0).map( () => null) );
data.piece = (new Array(16)).fill(true);

function setcell(y,x,c){
  data.board[y][x] = c;
  data.board.splice(y,1,data.board[y]);
}
import Board from "./components/board"
Vue.component("board", Board);

export default {
  data(){return data;},
  methods : {
    item2class
    
  }
  
}
  
</script>
<style scoped>

#leftpieces{
  width:200px;
  height:200px;
  display: flex;
  flex-flow: row wrap;
}

#board-root{
  display: flex;
  flex-flow: row wrap;
}
</style>