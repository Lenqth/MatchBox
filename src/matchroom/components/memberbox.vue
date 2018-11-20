<template>
  <div id="player-list" class="col2">
    <div class="group-detail">
      <div v-for=" (item,index) in player_slot" class="group-content" v-bind:class="{ joined : item.joined , ready : item.ready , 'group-content-you' : item.you }" v-on:click="item.you ? (item.ready=!item.ready,$emit('ready-changed')) : 0 ;"  :key="index" >
      </div>
    </div>
  </div>
</template>
<script>
import Vue from 'vue'

export default {
  props: ['player_slot']
}

</script>
<style>

@keyframes blinkborder {
  0% {border-color: rgba(255,255,255,1);}
  100% {border-color: rgba(255,255,255,0.2);}
}
.group-detail{
  display: flex;
  flex-flow: row wrap;
  width:300px;
  height:200px;
  border: 2px blue solid;
}
.group-content{
  box-sizing: border-box;
  flex-basis:50%;
  flex-shrink:1;
  flex-grow: 1;
}

.group-content-you{
  border-width:3px;
  border-style: solid;
  animation: blinkborder 0.7s ease 0.4s infinite alternate;
}

.group-content:nth-child(1).joined.ready{background-color: #ffcccc;}
.group-content:nth-child(2).joined.ready{background-color: #ccccff;}
.group-content:nth-child(3).joined.ready{background-color: #ccffcc;}
.group-content:nth-child(4).joined.ready{background-color: #ffccff;}
.group-content:nth-child(1).joined:not(.ready){background-color: #886666;}
.group-content:nth-child(2).joined:not(.ready){background-color: #666688;}
.group-content:nth-child(3).joined:not(.ready){background-color: #668866;}
.group-content:nth-child(4).joined:not(.ready){background-color: #886688;}

</style>
