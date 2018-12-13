<template> 
  <div class="root">
    <div class="opponent-hand">
      <card card_id="7" :open="open" @click.native="click_card"/> 
      <card card_id="7" :open="open" @click.native="click_card"/> 
      <card card_id="7" :open="open" @click.native="click_card"/> 
    </div>
    <div class="field">
      <card card_id="7" :open="open" @click.native="click_card"/> 
      <card card_id="7" :open="open" @click.native="click_card"/> 
      <card card_id="7" :open="open" @click.native="click_card"/> 
    </div>
    <div class="my-hand">
      <card card_id="7" :open="open" @click.native="click_card"/> 
      <card card_id="7" :open="open" @click.native="click_card"/> 
      <card card_id="7" :open="open" @click.native="click_card"/> 
    </div>
  </div>
</template>
<script>

import Vue from 'vue';
import Card from './components/card.vue'
Vue.component('card', Card)

var root = {"open":true};



export default {
  data(){
    return root;
  },
  methods:{
    click_card(id){
        this.open = !this.open
    }
  }
  
}
  
</script>
<style>
.card{
  width:10vh;
  height:15vh;
}
</style>
<style scoped>

.root{
  position: relative ;
  width: 100%;
  height: 100%;
}

.my-hand, .opponent-hand, .field{
  display: flex;
  position: absolute ;
  left:50%;
  transform: translateX(-50%);
}

.opponent-hand{
  top: 10%;
}
.field{
  top:50%;
  transform: translate(-50%);
}
.my-hand{
  bottom:10%;
}

</style>