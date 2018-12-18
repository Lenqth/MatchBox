<template>
  <div class="room-root flexbox">
    <audio id="sound1" preload="auto">
      <source src="@/assets/sounds/puu79_a.wav" type="audio/wav">
    </audio>
    <div class="col1">
      <textarea id="output" class="chat-output" rows="30"></textarea>
      <input type="text" id="txbox"><input type="button" value="send" id="sendbutton">
    </div>
    <memberbox v-bind:player_slot="player_slot" v-on:ready-changed="send_ready()"></memberbox>
  </div>
</template>
<script>
import Vue from 'vue'

import * as utils from './components/utils.js'
import memberbox from './components/memberbox.vue'
Vue.component('memberbox', memberbox)

var audio1 = document.getElementById('sound1')

var roominfo = { player_slot: [] }
var you = -1

function send_ready () {
  socket.send(JSON.stringify({'ready': roominfo.player_slot[you].ready}))
}
function writeln (x) {
  var el = document.getElementById('output')
  if (!el) return
  el.value += x + '\n'
}
function send (s) {
  var obj = {message: s}
  socket.send(JSON.stringify(obj))
}
var __vm = null
export default {
  name: 'MatchRoom',
  data () {
    return roominfo
  },
  methods: {
    send_ready
  },
  beforeRouteEnter (route, redirect, next) {
    next(vm => {
      __vm = vm
      if (!isRoomSocket(window.socket)) {
        set_event(new_socket())
      }else{
        set_event(window.socket)
      }
    })
  }
}
function isRoomSocket(socket){
  if(!socket) return false;
  if(socket.url.indexOf("room") >= 0 ){
    return true;
  }
  return false;
}

function new_socket() {
  var host = location.host
  if (location.port == 8080) { host = location.hostname + ':8000' }
  var socket = window.socket = new WebSocket('ws://' + (host) + '/jong/room/auto')
  return socket
}
function set_event(socket){
  socket.onmessage = h_onmessage
  socket.onerror = h_onerror
  socket.onclose = h_onclose
}

function h_onmessage (e) {
  var o = JSON.parse(e.data)
  if ('message' in o) {
    //    utils.play_sound("../assets/puu79_a.wav");
    var s1 = document.getElementById('sound1')
    if (s1) { s1.play() };
    writeln(o.message)
  }
  if ('roomsize' in o) {
    roominfo.player_slot = (new Array(o.roomsize).fill(0)).map(function () { return {'joined': false, 'ready': false, 'you': false, 'name': 'none'} })
  }
  if ('position' in o) {
    roominfo.player_slot[o.position].you = true
    you = o.position
    for (var [i, v] in o.room) {
      roominfo.player_slot[i].joined = true
    }
  }
  if ('room' in o) {
    for (var v of o.room) {
      roominfo.player_slot[v.position].joined = true
      roominfo.player_slot[v.position].ready = v.ready
    }
  }
  if ('joined' in o) {
    var dat = o.joined
    roominfo.player_slot[dat.position].joined = true
    roominfo.player_slot[dat.position].ready = dat.ready
  }
  if ('exited' in o) {
    var dat = o.exited
    roominfo.player_slot[dat.position].joined = false
  }
  if ('set_state' in o) {
    var stt = o.set_state
    var pos = stt.pos
    delete stt.pos
    for (var key in stt) {
      roominfo.player_slot[pos][key] = stt[key]
    }
  }
  if ('start' in o) {
    game_start(o.start)
  }
}
function h_onerror (e) { console.log('error:', e) }
function h_onclose (e) {
  console.log('close:', e)
  writeln('connection closed. please reload later.')
  for (var x of document.getElementsByClassName('group-content')) {
    x.classList.remove('joined')
    x.classList.remove('group-content-you')
  }
}
function send_click (e) {
  var x = document.getElementById('txbox').value
  document.getElementById('txbox').value = ''
  send(x)
  console.log(x)
}
function game_start (arg) {
  __vm.$router.push('/jong')
}

</script>
<style scoped>
.room-root{
  margin: 25px;
}

.flexbox{
  display: flex;
}
.col1{
  width:60%;
}
.chat-output{
  width:80%;
  height:40%
}
</style>
