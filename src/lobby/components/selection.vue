<template>
  <div class="control-selection">
    <div class="control-selection-title">{{title}}</div>
    <div v-for=" (item,index) in items" :key="index" class="control-selection-item"
         v-bind:class="{'control-selection-item-active':(item == selected)}"
         v-on:click="select(item)" >
      {{item}}
    </div>
  </div>
</template>
<script>

import Vue from 'vue';

export default {
  props:["title","items","default"],
  data: (vm) => ( {
    "selected": vm.default
  } ),
  methods:{
    select(item){
      console.log(item);
      this.selected = item;
      this.$emit("changed",item)
    }

  }

}

</script>
<style>
.control-selection{
  display:flex;
  height:30px;
}
.control-selection-title{
  margin:2px;
  min-width:140px;
  line-height: 30px;
}
.control-selection-item {
  margin:2px;
  min-width:30px;
  line-height: 30px;
  vertical-align: middle;
  border:1px black solid;
}
.control-selection-item-active{
  background-color: lightblue;
}
.control-selection-item:not(.control-selection-item-active){
  background-color: lightgray;
}
</style>
