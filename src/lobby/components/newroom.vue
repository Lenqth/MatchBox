<template>
  <div class="dialog-room">
    あああ
    <button v-on:click="closeThis()">CLOSE</button>
  </div>
</template>
<script>
import Vue from 'vue'

export default {
  props: ['player_slot'],

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
  width: 300px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
  transition: all .3s ease;
}

</style>
