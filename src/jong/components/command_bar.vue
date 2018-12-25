<template>
  <div style="width:100%;height:10%;">
    <transition-group class="command-bar clearfix" name="command">
      <div id="chow" key="chow" v-if="command_types_available.has('chow')" class="command" 
        @keydown.90="command('chow')" @click="command('chow')">チー(Z)</div>
      <div id="pong" key="pong" v-if="command_types_available.has('pong')" class="command" 
        @keydown.88="command('pong')" @click="command('pong');">ポン(X)</div>
      <div id="kong" key="kong" v-if="command_types_available.has('kong')" class="command" 
        @keydown.67="command('kong')" @click="command('kong');">カン(C)</div>
      <div id="conckong" key="conckong" v-if="command_types_available.has('conckong')" class="command" 
        @keydown.67="command('conckong')" @click="command('conckong');">暗カン(C)</div>
      <div id="apkong" key="apkong" v-if="command_types_available.has('apkong')" class="command" 
        @keydown.86="command('apkong')" @click="command('apkong');">加カン(V)</div>
      <div id="ron" key="ron" v-if="command_types_available.has('ron')" class="command" 
        @click="command('ron');">ロン</div>
      <div id="tsumo" key="tsumo" v-if="command_types_available.has('tsumo')" class="command" 
        @click="command('tsumo');">ツモ</div>
      <div id="skip" key="skip" v-if="command_types_available.has('skip')" class="command" 
        @click="command('skip');">スキップ</div>
    </transition-group>
  </div>
</template>

<script>

import Vue from 'vue';

export default {
  props:{
    "commands_available":{
      type:Array,
    }
  },
  methods:{
    command(x,head_type){
      this.$emit("command",x,head_type);
    }
  },
  computed:{
    command_types_available(){
      if(this.commands_available==null){
        return new Set();
      }
      return new Set(this.commands_available.map(x => x.type));
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

</style>