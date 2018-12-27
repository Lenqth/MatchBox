<template>
  <div :key="type_name" v-if="items!=null&&items.length>=1" class="command" 
        @keydown.90="clk()" @click="clk()" @mouseover="ovr()" @mouseleave="lev()">
        <slot/>{{items.length>=2?"△":""}}
        <transition name="meldpop">
          <div v-if="hover" class="meld-selection-popup">
            <exposedset v-for="(it,idx) in items" :key="idx" :tiles="it.tiles" :type="type_name" 
             @click.native="clk(it.pos)" style="margin:3px;"/>
          </div>
        </transition>
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
    "items":{
      type:Array,
    },
    "show_pattern":{
      type:Boolean,
      default:true
    }
  },
  data(){
    return {
      "hover":false
    }
  },
  computed:{

  },
  methods:{
    ovr(){
      if( this.show_pattern ){
        this.hover=true;
      }
    },
    lev(){
      if(this.hover){
        this.hover=false
      }
    },
    clk(x=null){
      if(this.items == null)return;
      if(this.items.length >= 2 ){
        if( x == null ){
          return;
        }else{
          this.hover=false;
          this.$emit("command",this.type_name,x);
        }
      }else{
        this.hover=false;
        this.$emit("command",this.type_name,this.items[0].pos);
      }
    }
  }
}
  
</script>

<style scoped>

.command-bar{
  display: flex;
  flex-wrap: nowrap;
  margin:3px 0;
  width:100%;
}
.command{
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