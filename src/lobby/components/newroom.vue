<template>
  <div class="dialog-room">
    <h2>部屋の作成</h2>
    ゲーム:
    <select name="type" class="selection" v-model="game_type">
      <option v-for="(item,index) in game_type_option" v-bind:value="item.id" :key="index" >{{item.name}}</option>
    </select>
    <div class="footer">
      <button v-on:click="closeThis()">CLOSE</button>
    </div>
  </div>
</template>
<script>
import Vue from 'vue'
import axios from 'axios'



var option = [ {"id":"jong","name":"中国麻雀"} ]
export default {
  props: {
    "game_type":{
      default : () => option[0].id ,
    },
    "game_type_option":{
      default : () => option ,
    },
  },

  methods: {
    closeThis () {
      this.$parent.dialogOpen = false
    },
    async getConfig (arg="") {
      if (location.port == 8080) { host = location.hostname + ':8000' }
      var response = await axios.get('http://'+host+'/jong/config/'+arg)
      var result = JSON.parse( response.data )


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
