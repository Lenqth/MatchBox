<template>
  <div style="width:100%;height:10%;" class="command-bar">
    <command-button key="ch" type_name="chow" :items="twc['chow']" @command="command" shortcut="90">チー(Z)</command-button>
    <command-button key="pn" type_name="pong" :items="twc['pong']" @command="command" shortcut="88">ポン(X)</command-button>
    <command-button key="kn" type_name="kong" :items="twc['kong']" @command="command" shortcut="67">カン(C)</command-button>
    <command-button key="ck" type_name="conckong" :items="twc['conckong']" @command="command" shortcut="67">暗槓(C)</command-button>
    <command-button key="ak" type_name="apkong" :items="twc['apkong']" @command="command" shortcut="86">加槓(V)</command-button>
    <command-button key="rn" type_name="ron" :items="twc['ron']" @command="command" :show_pattern="false">ロン</command-button>
    <command-button key="tm" type_name="tsumo" :items="twc['tsumo']" @command="command" :show_pattern="false">ツモ</command-button>
    <command-button key="sk" type_name="skip" :items="twc['skip']" @command="command" :show_pattern="false">スキップ</command-button>
  </div>
</template>

<script>

import Vue from 'vue';

import cbt from './command_button'
Vue.component('command-button', cbt)

export default {
  props:{
    "commands_available":{
      type:Array,
    }
  },
  methods:{
    command(type,head_ids){
      this.$emit("command",type,head_ids);
    }
  },
  computed:{
    command_types_available(){
      if(this.commands_available==null){
        return new Set();
      }
      return new Set(this.commands_available.map(x => x.type));
    },
    twc(){      
      if(this.commands_available==null){
        return {};
      }
      let res = {};
      for(let v of this.commands_available){
        if(res[v.type] == null){
          res[v.type] = [];
        }
        res[v.type].push(v);
      }
      return res;
    },
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