
import * as utils from './utils.js' ;


class AsyncConnection{
  constructor(href){
    this.socket = new WebSocket(href);;
    var bf = this.buffer = [];
    var cb = this.callbacks = [] ;
    this.socket.addEventListener("message" , function(e) {
      var o = JSON.parse(e.data);
      bf.push(o);
      var rem = [];
      for(var x in cb){
        if(bf.length>0){
          o = bf.shift();
          (cb[x])(o);
          rem.push(x);
        }
      }
      utils.take_positions(cb,rem);
    });
  }
}

AsyncConnection.prototype.send = function(obj){
  //console.log("send",obj);
  this.socket.send(JSON.stringify(obj));
}

AsyncConnection.prototype.receiveAsync = async function(){
  if(this.buffer.length>0){return this.buffer.shift();}
  var th = this;
  return await new Promise(function(resolve, reject) {
    th.callbacks.push(resolve);
  });
}

export class Deck{
  constructor(){
    this.players = new Array(4);
    this.turn = 0;
    this.nakimode = -1;
    this.subturn = -1;
    this.last_target = null;
    this.deck_left = 0 ;
    this.message = "*" ;
    this.prev_wind = 0;
    this.seat_wind = 0;
    this.yakulist = [];
    this.calculated_score = "";
    this.meld_selection = {type:"",meld_selection:[]};

    this.player_id = 0;

    this.time_left = null;
    this.timeout = null;

    for(let i=0;i<4;i++){
      this.players[i]=new Hand();
      this.players[i].id = i ;
    }
  }

}

Deck.prototype.start = async function(){
  this.conn = new AsyncConnection("ws://"+location.host+"/jong/room/"+document.forms[0].room_id);
  console.log( await this.conn.receiveAsync() );
  this.conn.send(JSON.stringify({"start":""}));
  while(true){
    res = await this.conn.receiveAsync();
    var pl = deck.players[deck.player_id];
    if(res.type == "reset"){
      delete res["reset"];
      this.assign(res);
    }if(res.type == "deck_left" ){
      this.deck_left = res.deck_left;
    }if(res.type == "claim_command" ){
      //{"commands_available": [{"type": 1, "pos": [[1], [2]]}], "_m_id": 7, "timeout": 1539616054.5650032}
      var tg_pl = res.target.player , tg_apkong = res.target.apkong , tg_tile = res.target.tile ;
      this.players[tg_pl].target = tg_apkong ? "apkong" : "trash" ;
      this.claim_target = tg_tile ;

      var commands = res.commands_available;
      this.players[this.player_id].commands_available = [ {type:"skip"} ].concat(res.commands_available);
      this.players[this.player_id].command_types_available = new Set( this.players[this.player_id].commands_available.map(x=>x.type) );
      this.players[this.player_id].allow_discard = false;

      var timeout = res.timeout * 1000 ;
      var cancelObj = {cancel:false};
      play_sound("puu79_a.wav");
      var input_res = await Promise.race( [claim_input(cancelObj) , timer(timeout,cancelObj)] );
      cancelObj.cancel = true;
      if( input_res != null ){
        input_res._m_id = res._m_id;
        console.log(input_res);
        this.conn.send(input_res);
      }
      this.players[tg_pl].target = null;
    }else if( res.type == "agari" ){

    }else if( res.type == "expose" ){
      this.players[res.pid].exposed.push( res.obj );
    }else if( res.type == "apkong" ){
      var ex = this.players[res.pid].exposed;
      for(var v of ex){
        if( v.type == "pong" && v.tiles[0] == res.tile ){
          v.tiles.push(res.tile);
          v.type="apkong";
          break;
        }
      }
    }else if( res.type == "discard" ){
      play_sound("clock04.wav");
      this.players[res.pid].trash.push(res.tile);
    }else if( res.type == "your_turn" ){
      // {"hand_tiles": [2, 4, 5, 6, 19, 22, 24, 34, 34, 38, 49, 52, 53], "draw": 22, "turn_commands_available": null, "_m_id": 4, "timeout": 1539603590.1542008}
      this.players[this.player_id].hand = res.hand_tiles;
      this.players[this.player_id].drawed = res.draw;
      this.players[this.player_id].commands_available = res.turn_commands_available == null ? [] : res.turn_commands_available ;
      this.players[this.player_id].command_types_available = new Set( this.players[this.player_id].commands_available.map(x=>x.type) );
      this.players[this.player_id].allow_discard = true;

      var timeout = res.timeout * 1000 ;
      var cancelObj = {cancel:false};
      play_sound("puu79_a.wav");
      var input_res = await Promise.race( [turn_input(cancelObj) , timer(timeout,cancelObj)] );
      cancelObj.cancel = true;
      console.log(input_res);
      if( input_res != null ){
        input_res._m_id = res._m_id;
        this.conn.send(input_res);
      }else{
        pl.trash_tile(-1);
      }

      //await turn_input(this.player_id);

    }
  }
}



Deck.prototype.sampleset = function(){
  var smpl = {"deck_left": 136, "player_id": 0, "seat_wind": 0, "prev_wind": 0, "players": [{"hand": [2, 39, 55, 54, 54, 35, 6, 3, 24, 8, 9, 1, 18], "drew": null, "trash": [], "exposed": [], "flower": 0}, {"hand": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "trash": [], "exposed": [], "flower": 0}, {"hand": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "trash": [], "exposed": [], "flower": 0}, {"hand": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "trash": [], "exposed": [], "flower": 0}]};
  this.assign(smpl);
}

Deck.prototype.assign = function(obj){
  for(var k in obj){
    if( k == "players" ){
      for( var i = 0 ; i < 4 ; i++ ){
          this.players[i].assign( obj.players[i] ) ;
      }
    }else{
      this[k] = obj[k];
    }
  }
}



Deck.prototype.resyncdata = async function(conn){
  this.conn = conn ;
  AsyncConnection.send( {"type":"get_all"} );
  var res = AsyncConnection.receiveAsync();
  this.assign(res);
}


Deck.numtosrc_table =
                   ["back", "man1", "man2", "man3", "man4", "man5", "man6", "man7", "man8", "man9", "back", "back", "back", "back", "back", "back",
                    "[16]", "pin1", "pin2", "pin3", "pin4", "pin5", "pin6", "pin7", "pin8", "pin9","back", "back", "back", "back", "back", "back",
                    "[32]", "sou1", "sou2", "sou3", "sou4", "sou5", "sou6", "sou7", "sou8", "sou9","back", "back", "back", "back", "back", "back",
                    "[48]", "ji1", "ji2", "ji3", "ji4", "ji5", "ji6", "ji7", "[38]","[39]","back", "back", "back", "back", "back", "back",
                    "[64]", "hana", "hana", "hana", "hana", "hana", "hana", "hana", "hana", "all","back", "back", "back", "back", "back", "back"];




class Hand{
  constructor(){
    this.id = -1;
    this.hand = [];
    this.trash = [];
    this.exposed = [];
    this.pullout = [];
    this.drawed = null ;
    this.skip_draw = false;
    this.konged = false;
    this.kousei = null;
    this.yakulist = null;
    this.yakuscore = null;

    this.allow_discard = false;
    this.commands_available = [];
    this.command_types_available = new Set();

    this.open = false;

    this.target = null ;
  }
  assign(obj){
    // hand: Array(13), drew: null, trash: Array(0), exposed: Array(0), flower: 0
    this.hand = obj.hand ;
    this.drawed = obj.drew ;
    this.trash = obj.trash ;
    this.exposed = obj.exposed ;
    this.flower = obj.flower ;

  }
  trash_tile(pos){
    if( pos == -1 ){
      this.drawed = null;
    }else{
      this.hand.splice(pos,1) ;
      this.hand.push( this.drawed );
      this.drawed = null;
    }
    this.hand.sortnum();
  }

}


var _wind_name = ["東","南","西","北"];
export function get_wind_name(id){
  return _wind_name[id];
}

export function tile_click(x){
  var pl = deck.players[deck.player_id];
  var pos = parseInt( x.getAttribute("pos") );
  if(input_resolve != null && pl.allow_discard ){
    input_resolve("discard",pos);
  }
}

export async function click_meld_popup(pos){
  console.log("meld-select:"+pos.toString());
  if(input_resolve != null){
    deck.meld_selection.meld_selection = [] ;
    input_resolve(deck.meld_selection.type , deck.meld_selection.pos[pos] );
  }
}

export function command(type){
  if(input_resolve == null){return;}
  var pl = deck.players[deck.player_id];
  var cmd = pl.commands_available;
  var fil = cmd.filter( x => (x.type == type) );
  if(fil.length == 0){return;}
  if(fil.length == 1){
    input_resolve(type,fil[0].pos);
    return;
  }else{
    var selections = fil.map( x => x.pos );
    var tiles = selections.map( x => x.map( y => y >= 0 ? pl.hand[y] : ( y == -1 ? pl.drawed : deck.claim_target ) ) );
    deck.meld_selection.type = type ;
    deck.meld_selection.meld_selection = tiles ;
    deck.meld_selection.pos = selections ;
  }
}


var input_resolve = null;
export async function claim_input(){
  return new Promise(
    function(resolve,reject){
      input_resolve = function(type,value){
        input_resolve = null;
        resolve( {"type":type,"pos":value} );
      };
    }
  )
}

export async function turn_input(){
  return new Promise(
    function(resolve,reject){
      input_resolve = function(type,value){
        var pl = deck.players[deck.player_id];
        if( type == "discard" ){
          if( ( pl.drawed != null && value == -1 ) || ( 0 <= value < pl.hand.length ) ){
            pl.trash_tile(value);
            input_resolve = null;
            pl.allow_discard = false;
            resolve( {"type":"discard","pos":value} );
          }
        }else{
          input_resolve = null;
          pl.allow_discard = false;
          resolve( {"type":type,"pos":value} );
        }
      };
    }
  )
}


export function timer_interval(resolve,timeout,cancelObj){
  var left = deck.time_left = Math.floor( ( timeout - (new Date()).getTime() ) / 100 ) / 10 ;
  if( left < 0 ){
    console.log("!!timeout!!");
    deck.time_left = null;
    resolve();
  }
  if(cancelObj.cancel){
    deck.time_left = null;
    resolve();
  }
}

export async function timer(timeout,cancelObj){
  var cancel = null;
  await new Promise( (resolve,reject) => {cancel = setInterval( () => timer_interval(resolve,timeout,cancelObj) , 100 )  } );
  clearInterval(cancel);
  return null;
}
// timer( (new Date()).getTime() + 10000 );

