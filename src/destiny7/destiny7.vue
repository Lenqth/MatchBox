<template>
    <card card_id="7" :open="open" @click.native="click_card" width=100 height=150 /> 
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
<style scoped>

</style>