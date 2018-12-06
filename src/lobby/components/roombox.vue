<template>
  <div class="room" v-bind:class="{'room-full':is_full}" >
    <div class="room-top">
      <div class="room-title">{{room.room_id}}</div>
      <div class="room-cap">{{room.room_pop}} / {{room.room_cap}}</div>
    </div>
    <div class="room-body">
      
    </div>   
  </div>
</template>
<script>

import Vue from 'vue';

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
.room:hover:not(.room-full){
  background-color: #aaaadd ;
}

.room-top{
  width: 100%;
  display: flex;

}

.room-title{
  width:88%;
  overflow: hidden;
}

.room-cap{
  box-sizing: border-box;
  border-left: 2px solid black;
  width: 12%;

}

.room-body{
  min-height:4em;

}

</style>