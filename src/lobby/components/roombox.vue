<template>
  <v-card class="room" :class="{'room-full':is_full}" width="300" color="#ccccdd">
    <div class="room-top">
      <div class="room-title">{{room.room_id}}</div>
      <div class="room-cap">{{room.room_pop}} / {{room.room_cap}}</div>
    </div>
    <div class="room-body">              
    </div>   
  </v-card>
</template>
<script>

import Vue from "vue";
import Vuetify from 'vuetify'
Vue.use(Vuetify);

export default {
  props : ["room"],
  data: () => ({
  }),
  computed :{
    is_full(){
      return ( this.room.room_pop == this.room.room_cap ) ;
    }

  }
}
  
</script>
<style scoped>

.room{
  box-sizing: border-box;
  /* border: 1px solid black; */
}
.room-full{
  background-color: magenta ;
}


.room-top{
  width: 100%;
  display: flex;
}
.room-title{
  width:84%;
  overflow: hidden;
}
.room-cap{
  box-sizing: border-box;
  border-left: 2px solid black;
  width: 16%;

}

.room-body{
  min-height:4em;
}

</style>