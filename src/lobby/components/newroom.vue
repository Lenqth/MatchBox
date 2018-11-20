<template>
  <div class="dialog-room">
    <h2>部屋の作成</h2>
    ゲーム:
    <select name="type" class="selection">
      <option v-for="(item,index) in game_type" value="item.id" :key="index" >{{item.name}}</option>
    </select>
    <div class="footer">
      <button v-on:click="closeThis()">CLOSE</button>
    </div>
  </div>
</template>
<script>
import Vue from 'vue'
import axios from 'axios'

export default {
  props: {
    "game_type":{ 
      default : () => [ {"id":"jong","name":"中国麻雀"} ] , 
    },
  },

  methods: {
    closeThis () {
      this.$parent.dialogOpen = false
    }
  }
}

</script>
<style>

.dialog-room{
  background-color: lightgray;
  width: 600px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
  transition: all .3s ease;
}
.selection{
  min-width:200px;

}

.footer{
  margin-top:50px;
}

</style>
