<template>
  <div :key="type_name" class="command" :class="{checked:value}" 
        @click="clk()">
        <slot/>
  </div>
</template>

<script>

import Vue from 'vue';

import exposedset from './exposedset'
Vue.component('exposedset', exposedset)

export default {
  props:{
    "type_name":{
      type:String,
    },
    "value":{
      type:Boolean,
      default:false
    }
  },
  computed:{

  },
  methods:{
    clk(x=null){
      this.$emit("input",!this.value)
    }
  }
}
  
</script>

<style scoped>

.command{
  user-select: none;
  position: relative;
  background-color: white;
  border:1px black solid;
  font-size: 100%;
  flex-basis:15%;
  height: 100%;
}
.command-enter-active{
  transition: height 0.6s 0s ease;
}
.checked{
  background-color: skyblue !important;
}

.command-leave-active{
  transition: height 0.6s 0s ease;
}

.command-enter , .command-leave-to{
  height: 0px;
}

.player-hand:not(.player-main){
  visibility: hidden;
}

.meld-selection-popup{
  position:absolute;
  background-color:darkgrey;
  bottom:100%;
  min-width: 100%;
}
.meld-selection-popup .exposed-group:not(:hover){
  border: 3px transparent solid;
}
.meld-selection-popup .exposed-group:hover{ 
  border: 3px red solid;
}

.meldpop-enter-active{
  animation-name: stretch-xy-in;
	animation-timing-function: ease-in;
  animation-duration: 0.4s;
}
.meldpop-leave-active{
  animation-name: stretch-xy-in;
	animation-direction: reverse;
	animation-timing-function: ease-out;
  animation-duration: 0.4s;
}
@keyframes stretch-xy-in {
	0% {
    transform: scale(0);
    transform-origin: left bottom;
  }
	100% {
    transform: scale(1);
    transform-origin: left bottom;
	}	
}


</style>