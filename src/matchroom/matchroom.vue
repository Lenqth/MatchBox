<template>
  <div id="room-root" class="flexbox">
    <div class="col1">
      <textarea id="output" rows="40"></textarea>
      <input type="text" id="txbox"><input type="button" value="send" id="sendbutton">
    </div>
    <memberbox v-bind:player_slot="player_slot" v-on:ready-changed="send_ready()"></memberbox>
  </div>
</template>
<script>
import Vue from 'vue'; 

import * as utils from './components/utils.js' ;
import memberbox from './components/memberbox.vue'
Vue.component('memberbox',memberbox);

var audio1 = document.getElementById("sound1") ;

var roominfo = { player_slot : [] };
var you = -1;

function send_ready(){
  socket.send(JSON.stringify({"ready":roominfo.player_slot[you].ready}));
}
function writeln(x){
  document.getElementById("output").value += x + "\n" ;
}
function send(s){
  var obj={message:s};
  socket.send(JSON.stringify(obj));
}

export default {
  name: 'MatchRoom',
  data(){
    return roominfo;
  },
  methods:{
    send_ready
  }
}
window.socket = new WebSocket("ws://"+(location.hostname + ":" + "8000")+"/jong/room/nyan");


socket.onmessage = function(e) {
  var o = JSON.parse(e.data);
  if("message" in o){
    utils.play_sound("../assets/puu79_a.wav");
    writeln(o.message);
  }
  console.log(o);
  if("roomsize" in o){
    roominfo.player_slot = (new Array( o.roomsize ).fill(0) ).map( function(){return {"joined":false,"ready":false,"you":false,"name":"none"};} );
  }
  if("position" in o){
    roominfo.player_slot[o.position].you = true;
    you = o.position;
    for(var [i,v] in o.room ){
      roominfo.player_slot[i].joined = true;
    }
  }
  if("room" in o){
    for( var v of o.room ){
      roominfo.player_slot[v.position].joined = true;
      roominfo.player_slot[v.position].ready = v.ready;
    }
  }
  if("joined" in o){
    var dat = o.joined ;
    roominfo.player_slot[dat.position].joined = true;
    roominfo.player_slot[dat.position].ready = dat.ready;
  }
  if("exited" in o){
    var dat = o.exited ;
    roominfo.player_slot[dat.position].joined = false;
  }
  if("set_state" in o){
    var stt = o.set_state;
    var pos = stt.pos;
    delete stt.pos;
    for( var key in stt ){
      roominfo.player_slot[pos][key] = stt[key];
    }
  }
}

socket.onerror = function(e) {console.log("error:",e);}
socket.onclose = function(e) {
  console.log("close:",e);
  writeln("connection closed. please reload later.");
  for(var x of document.getElementsByClassName("group-content") ){
    x.classList.remove("joined");
    x.classList.remove("group-content-you");
  }
}
function send_click(e){
  var x = document.getElementById("txbox").value;
  document.getElementById("txbox").value="";
  send(x);
  console.log(x);
}
socket.onopen = function() {
}

</script>
<style>
.navbar{
  width:100%;
  height:40px;
  background-color: gray;
  margin: 0px 0px 20px;
  color : white;
}
.login-disp{
  text-align:right;
  margin:10px;
}

.flexbox{
  display: flex;

}
.col1{
  width:60%;
}
.col2{

}
#output{
  width:80%;
  height:40%
}
</style>