
class Deck{
  constructor(){
    this.players = new Array(4);
    this.turn = 0;
    this.nakimode = -1;
    this.subturn = -1;
    this.last_target = null;
    this.reset();
    for(let i=0;i<4;i++){
      this.players[i]=new Hand();
      this.players[i].id = i ;
      this.players[i].hand = this.get_init(13);
    }
    for(let i=0;i<4;i++){
      let n = 0;
      do{
        n = this.players[i].pullout_all(this);
        this.players[i].hand = this.players[i].hand.concat(this.get_init(n));
      }while(n>0);
    }
    this.players[0].drawed = this.take();
    for(let i=0;i<4;i++){
      this.players[i].hand.sortnum();
      this.players[i].redraw();
    }
    for(let i=1;i<4;i++){
      this.players[i].ai = new AIRandom(this.players[i]);
    }
    this.proc = this.__proc();
  }
  reset(){
    let ary=[];
    for(let i=1;i<=9;i++){ // MAN
      ary.push(i);ary.push(i);ary.push(i);ary.push(i);
    }
    for(let i=11;i<=19;i++){ // SOU
      ary.push(i);ary.push(i);ary.push(i);ary.push(i);
    }
    for(let i=21;i<=29;i++){ // PIN
      ary.push(i);ary.push(i);ary.push(i);ary.push(i);
    }
    for(let i=31;i<=37;i++){ // NEWS-RGW
      ary.push(i);ary.push(i);ary.push(i);ary.push(i);
    }
    for(let i=41;i<=48;i++){ // flower
      ary.push(i);
    }
    this.all_tiles = ary.slice();
    this.message = "プレイヤー"+this.turn+"のターン";
    this.array = shuffle(ary);
  }
  get_init(n){
    return this.array.splice(0,n);
  }

  take(){
    return this.array.shift();
  }
  reset_command(){
      this.tsumo = new Array(4).fill(false);
      this.conckong = new Array(4).fill([]);
      this.apkong = new Array(4).fill([]);
      this.chow = new Array(4).fill([]);
      this.pong = new Array(4).fill([]);
      this.kong = new Array(4).fill([]);
      this.ron = new Array(4).fill(false);
      this.skip = new Array(4).fill(true);
  }

  check_turn_command(){
    this.reset_command();
    this.tsumo[this.turn] = this.players[this.turn].is_agari(this.players[this.turn].drawed);
    this.conckong[this.turn] = this.players[this.turn].chk_conckong();
    this.apkong[this.turn] = this.players[this.turn].chk_apkong();
  }

  check_tile(tile,is_chankong){
    this.reset_command();
    this.trashed_tile = tile;
    //console.log(this.trashed_tile);
    if(is_chankong){
      let f = false;
      for(let i=0;i<4;i++){
        if( i == this.turn )continue;
        this.ron[i] = this.players[i].is_agari(tile);
        if(this.ron[i])f = true;
      }
      return f;
    }else{
      this.chow[(this.turn+1)%4] = this.players[ (this.turn+1)%4 ].chk_chow(tile);
      for(let i=0;i<4;i++){
        if( i == this.turn )continue;
        this.pong[i] = this.players[i].chk_pong(tile);
        this.kong[i] = this.players[i].chk_kong(tile);
        this.ron[i] = this.players[i].is_agari(tile);
      }
    }
  }

  claim_tile(pl_id,type_name,pattern){
    if(type_name=="ron"){this.agari(pl_id);return;}
    this.players[pl_id].claim_tile(type_name,pattern,this.trashed_tile);
    this.turn = pl_id;
    this.subturn = -1;
    this.trashed_tile = null;
    this.claimed = true;
  }

  agari(pl_id){

  }

  set_target(o){
    this.clear_target();
    o.target = true ;
    this.last_target = o;
  }
  clear_target(){
    if(this.last_target!=null){
      this.last_target.target = null;
      this.last_target = null;
    }
  }

}

Deck.prototype.__proc = async function*(){
  while(true){
    if(this.players[this.turn].skip_draw){
      this.players[this.turn].skip_draw=false;
    }else{
      let retry = false;
      do{
        this.players[this.turn].drawed = this.take();
        retry = this.players[this.turn].pullout_auto();
        this.players[this.turn].hand.sortnum();
      }while(retry);
      this.check_turn_command();
    }
    this.claimed = false;
    if( "ai" in this.players[ this.turn ] ){
      let pl = this.players[ this.turn ];
      pl.trash_tile( pl.ai.get_discard_pos() );
    }else{
      //if( this.tsumo[i] || this.apkong[i].length>0 || this.conckong[i].length>0 ){
      this.skip[0]=false;
      command_open();
      //console.log("yield (discard)");
      yield null;
      command_close();
      this.skip[0]=true;
      //}
    }
    await play_sound("clock04.wav");
    if( this.players[this.turn].drawed != null ){
      this.players[this.turn].hand.push(this.players[this.turn].drawed);
      this.players[this.turn].hand.sortnum();
      this.players[this.turn].drawed = null;
    }
    if(this.claimed){
      continue;
    }
    this.claimed = false;
    this.command = new Array(4).fill(null);
    for(let i=0;i<4;i++){
      if( this.chow[i].length>0 || this.pong[i].length>0 || this.kong[i].length>0 || this.ron[i] ){
        this.subturn = i;
        if(i==0){
          command_open();
          await play_sound("puu79_a.wav");
          //console.log("yield (command)");
          yield null;
          command_close();
        }else{
          // ai command
        }
      }
    }
    this.clear_target();
    command_proc:{
      for(let i=0;i<4;i++){
        if( this.command[i] != null && ( this.command[i][1] == "ron" )){
          this.claim_tile.apply(this,this.command[i]);
          break command_proc;
        }
      }
      for(let i=0;i<4;i++){
        if( this.command[i] != null && ( this.command[i][1] == "minkong" || this.command[i][1] == "pong" ) ){
          this.claim_tile.apply(this,this.command[i]);
          break command_proc;
        }
      }
      for(let i=0;i<4;i++){
        if( this.command[i] != null && ( this.command[i][1] == "chow" ) ){
          this.claim_tile.apply(this,this.command[i]);
          break command_proc;
        }
      }
    }
    if( this.apkong_gen != null ){
      this.apkong_gen.next();
      this.apkong_gen = null;
    }
    if(!this.claimed){
      this.turn++;
      this.turn %= 4;
    }
    this.reset_command();
    this.trashed_tile = null;
    this.subturn = -1;
    this.message = "プレイヤー"+this.turn+"のターン";
    if( this.array.length == 0 ){
      this.message = "流局です";
      return;
    }
    for(let i=0;i<4;i++){
      this.players[i].redraw();
    }
    if( "ai" in this.players[ this.turn ] ){
      await taskSleep(200);
    }
  }
}



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

    this.open = false;
    this.redraw();
  }

  //get hand(){ return this._hand; } set hand(value){ this._hand = value; }
  //get trash(){ return this._trash; } set trash(value){ this._trash = value; }
  //get exposed(){ return this._exposed; } set exposed(value){ this._exposed = value; }
  //get pullout(){ return this._pullout; } set pullout(value){ this._pullout = value; }
  //get drawed(){ return this._drawed; } set drawed(value){ this._drawed = value; }

  trash_tile(pos){
    let o = {};
    o.tsumogiri = false;
    o.yoko = false;
    o.target = false;
    this.konged = false;
    if( pos == -1 ){
      o.id = this.drawed;
      o.tsumogiri = true;
      this.trash.push( o ) ;
      this.drawed = null;
    }else{
      o.id = this.hand.splice(pos,1)[0] ;
      this.trash.push( o ) ;
    }
    this.hand.sortnum();
    deck.check_tile(o.id);
    deck.set_target(o);
    this.redraw();
  }

  pullout_auto(){
    if(deck.array.length == 0)return false;
    if( get_suit(this.drawed) == "FLOWER" ){
      this.pullout.push(this.drawed);
      this.drawed=null;
      return true;
    }
    for(let k in this.hand){
      if( get_suit(this.hand[k]) == "FLOWER" ){
        this.pullout.push(this.hand[k]);
        this.hand.splice(this.hand[k],1);
        return true;
      }
    }
    return false;
  }
  pullout_all(deck){
    let pos = [];
    for(let k in this.hand){
      if( get_suit(this.hand[k]) == "FLOWER" && deck.array.length > 0 ){
        this.pullout.push(this.hand[k]);
        pos.push(k);
      }
    }
    pos.sort( (x,y) => y-x );
    for(let k of pos){
      this.hand.splice(k,1);
    }
    return pos.length;
  }
  is_menzen(){
    return this.exposed.filter( x=> x["type"]!="conckong" ).length==0;
  }

  chk_chow(tile){
    let num = get_number(tile);
    let l = this.hand.length;
    let res = [],s=new Set();
    for(let i=0;i<l-1;i++){
      for(let j=i+1;j<l;j++){
        if( is_consecutive([tile,this.hand[i],this.hand[j]]) ){
          let str = [this.hand[i],this.hand[j],tile].sort((x,y)=>x-y).join(",") ;
          if(!s.has(str)){
            res.push( [i,j] );
            s.add(str);
          }
        }
      }
    }
    return res;
  }

  chk_pong(tile){
    let num = get_number(tile);
    let l = this.hand.length;
    let res = [];
    for(let i=0;i<l-1;i++){
      for(let j=i+1;j<l;j++){
        if( tile == this.hand[i] && tile == this.hand[j] ){
          res.push( [i,j] );
        }
      }
    }
    return res;
  }
  chk_kong(tile){
    let num = get_number(tile);
    let l = this.hand.length;
    let res = [];
    for(let i=0;i<l-2;i++){
      for(let j=i+1;j<l-1;j++){
        for(let k=j+1;k<l;k++){
          if( tile == this.hand[i] && tile == this.hand[j] && tile == this.hand[k] ){
            res.push( [i,j,k] );
          }
        }
      }
    }
    return res;
  }

  chk_apkong(){
    let h = this.hand.slice();
    let l = this.hand.length;
    let res = [];
    for(let v of this.exposed){
      if( v.type == "pong" ){
        let p = this.hand.indexOf(v.tiles[0]);
        if( p >= 0 ){
          res.push( { pos : p , appendto : v } );
        }else if( v.tiles[0] == this.drawed ){
          res.push( { pos : -1 , appendto : v }  );
        }
      }
    }
    return res;
  }
  chk_conckong(){
    let h = this.hand.slice();
    if(this.drawed!=null){
      var di = h.length;
      h.push(this.drawed);
    }
    let l = h.length;
    let res = [];
    let [ std , idx ] = sort_correspond( h.slice() );
    if(this.drawed!=null){
      idx[idx.indexOf(di)]=-1;
    }
    let run = [] , runo = null ;
    for( let i = 0; i < l ; i++ ){
      if( std[i] == runo ){
        run.push( idx[i] );
      }else{
        if( run.length >= 4 ){
          res.push( run.slice(0,4) );
        }
        run=[idx[i]];
        runo = std[i];
      }
    }
    if( run.length >= 4 ){
      res.push( run.slice(0,4) );
    }
    return res;
  }

  claim_tile(type_name,pattern,tile){
    console.log(pattern);
    if( type_name != "minkong" ){
      this.skip_draw = true;
    }else{
      this.konged = true;
    }
    var piz =  take_positions( this.hand , pattern ) ;
    piz.push(tile);
    this.exposed.push( {type:type_name,tiles:piz} );
    this.hand.sortnum();
    this.redraw();
  }
  do_conckong(pattern){
    let l = pattern.length;
    let p = pattern.slice();
    let tils=[];
    let k = p.indexOf(-1);
    if(k!=-1){
      p.splice(k,1);
      tils.push( this.drawed );
      this.drawed = null;
    }
    tils = tils.concat( take_positions(this.hand,p) );
    this.exposed.push( {type:"conckong",tiles:tils} );
    deck.claimed = true;
    this.konged = true;
  }
  is_agari(tile){
    // normal agari
    if( deck.turn == this.id ){ // ツモ
      this.agari_tile = this.drawed ;
      this.agari_tsumo = true;
    }else{
      this.agari_tile = deck.trashed_tile ;
      this.agari_tsumo = false;
    }
    let kousei = mentu_kousei( this.hand.concat(tile) , this );
    if( kousei.length == 0 ){
      return false;
    }
    this.kousei = kousei;
    let max_li = [];
    let max_v = 0;
    let machi = calc_machi(this);
    this.machi_single = machi.length==1;
    for(let x of kousei){
      var [v,li] = yakucheck(this,x);
      if(v>max_v){
        max_v = v;
        max_li = li;
      }
    }
    this.yakulist = max_li;
    this.yakuscore = max_v;
    yaku_disp.score = max_v;
    yaku_disp.list = max_li;
    return true;
  }
  redraw(){}

  do_apkong(pos,appendto){
    let gen = this.__internal_apkong(pos,appendto);
    if(!gen.next().done){
      deck.apkong_gen = gen;
    }
  }
}
Hand.prototype.__internal_apkong = function*(pos,appendto){
  let tile = null;
  if(pos>=0){
    tile = this.hand.splice(pos,1)[0];
  }else{
    tile = this.drawed;
    this.drawed = null;
  }
  if( appendto.type != "pong" ){
    throw null;
  }

  if( deck.check_tile(tile) ){ // 槍槓チェック
    deck.chankong = true;
    yield;
  }
  appendto.tiles.push(tile);
  appendto.type = "apkong";
  deck.claimed = true;
  this.konged = true;
}

function anim_show(id,flg){
  document.getElementById(id).classList.remove("anim-show");
  document.getElementById(id).classList.remove("anim-hide");
  if(flg){
    document.getElementById(id).classList.add("anim-show");
  }else{
    document.getElementById(id).classList.add("anim-hide");
  }
}

function command_open(){
  console.log("claim-check");
  command_locked = false;
  //anim_show("my-command",true);
  anim_show("chow",deck.chow[0].length>0);
  anim_show("pong",deck.pong[0].length>0);
  anim_show("kong",deck.kong[0].length>0);
  anim_show("ron",deck.ron[0]);
  anim_show("tsumo",deck.tsumo[0]);
  anim_show("conckong",deck.conckong[0].length>0);
  anim_show("apkong",deck.apkong[0].length>0);

  anim_show("skip",deck.skip[0]);
}

function command_close(){
  anim_show("chow",false);
  anim_show("pong",false);
  anim_show("kong",false);
  anim_show("ron",false);

  anim_show("tsumo",false);
  anim_show("conckong",false);
  anim_show("apkong",false);

  anim_show("skip",false);
}

var meld_selection = {type:"",meld_selection:[]};

async function click_meld_popup(pos){
  if(meld_selection.type == "conckong"){
    popup_box_down();
    command_close();
    deck.players[0].do_conckong(deck.conckong[0][pos]);
    await deck.proc.next();
    return;
  }else if(meld_selection.type == "apkong"){
    popup_box_down();
    command_close();
    let p = deck.apkong[0][pos];
    deck.players[0].do_apkong(p.pos,p.appendto);
    await deck.proc.next();
    return;
  }
  deck.command[0] = [ 0, meld_selection.type , deck.chow[0][pos] ];
  popup_box_down();
  command_close();
  await deck.proc.next();
}

var command_locked = true;

async function command(t){
  if(command_locked)return;
  command_locked = true;
  if(t == "skip"){
    if(!deck.skip[0])return;
    command_close();
    deck.command[0] = null;
    await deck.proc.next();
  }else if( t == "chow" ){
    if(deck.chow[0].length==0)return;
    if(deck.chow[0].length>1){
      meld_selection.type="chow";
      meld_selection.meld_selection = deck.chow[0].map( x=> [deck.players[0].hand[x[0]],deck.players[0].hand[x[1]],deck.trashed_tile].sortnum() );
      popup_box_up();
      return;
    }
    deck.command[0] = [ 0,"chow",deck.chow[0][0] ];
    command_close();
    await deck.proc.next();
  }else if( t == "pong" ){
    if(deck.pong[0].length==0)return;
    deck.command[0] = [ 0,"pong",deck.pong[0][0] ];
    command_close();
    await deck.proc.next();
  }else if( t == "kong" ){
    if(deck.kong[0].length==0)return;
    deck.command[0] = [ 0,"minkong",deck.kong[0][0] ];
    command_close();
    await deck.proc.next();
  }else if( t == "ron" ){
    deck.command[0] = [ 0,"ron"];
  }else if( t == "apkong" ){
    if(deck.apkong[0].length==0)return;
    if(deck.apkong[0].length>1){
      meld_selection.type="apkong";
      meld_selection.meld_selection = deck.apkong[0].map( x=> [deck.players[0].hand[x.pos]].sortnum() );
      popup_box_up();
      return;
    }
    command_close();
    let p = deck.apkong[0][0];
    deck.players[0].do_apkong(p.pos,p.appendto);
    await deck.proc.next();
  }else if( t == "conckong" ){
    if(deck.conckong[0].length==0)return;
    if(deck.conckong[0].length>1){
      meld_selection.type="conckong";
      meld_selection.meld_selection = deck.conckong[0].map( x=> [deck.players[0].hand[x[0]]].sortnum() );
      popup_box_up();
      return;
    }
    deck.players[0].do_conckong(deck.conckong[0][0]);
    command_close();
    await deck.proc.next();
  }else if( t == "tsumo" ){
    deck.agari();
  }
}

async function tile_click(x){
  if(deck.turn != 0) return;
  if(deck.subturn != -1) return;
  var pos = x.getAttribute("pos");
  //console.log(pos);
  deck.players[0].trash_tile(pos);
  await deck.proc.next();
}

document.onkeydown = keydown;

function keydown(e){
  let k = e.keyCode;
  switch(k){
    case 27: //esc
    case 32: // space
      command("skip");
      break;
    case 90: //Z
      command("chow");
      break;
    case 88: //X
      command("pong");
      break;
    case 67: //C
      command("kong");
      break;

  }
}


Deck.numtotile_table_old =
                  ["[00]", "🀇", "🀈", "🀉", "🀊", "🀋", "🀌", "🀍", "🀎", "🀏",
                   "[10]", "🀐", "🀑", "🀒", "🀓", "🀔", "🀕", "🀖", "🀗", "🀘",
                   "[20]", "🀙", "🀚", "🀛", "🀜", "🀝", "🀞", "🀟", "🀠", "🀡",
                   "[30]", "🀀", "🀁", "🀂", "🀃", "🀆", "🀄", "🀅", "[38]","[39]",
                   "[40]", "🀢", "🀣", "🀤", "🀥", "🀦", "🀧", "🀨", "🀩", "🀪", "🀫"];
/*
Deck.numtotile_table =
                   ["[00]", __img("man1"), __img("man2"), __img("man3"), __img("man4"), __img("man5"), __img("man6"), __img("man7"), __img("man8"), __img("man9"),
                    "[10]", __img("sou1"), __img("sou2"), __img("sou3"), __img("sou4"), __img("sou5"), __img("sou6"), __img("sou7"), __img("sou8"), __img("sou9"),
                    "[20]", __img("pin1"), __img("pin2"), __img("pin3"), __img("pin4"), __img("pin5"), __img("pin6"), __img("pin7"), __img("pin8"), __img("pin9"),
                    "[30]", __img("ji1"), __img("ji2"), __img("ji3"), __img("ji4"), __img("ji5"), __img("ji6"), __img("ji7"), "[38]","[39]",
                    "[40]", __img("hana"), __img("hana"), __img("hana"), __img("hana"), __img("hana"), __img("hana"), __img("hana"), __img("hana"), __img("all")];
*/
Deck.numtosrc_table =
                   ["back", "man1", "man2", "man3", "man4", "man5", "man6", "man7", "man8", "man9",
                    "[10]", "sou1", "sou2", "sou3", "sou4", "sou5", "sou6", "sou7", "sou8", "sou9",
                    "[20]", "pin1", "pin2", "pin3", "pin4", "pin5", "pin6", "pin7", "pin8", "pin9",
                    "[30]", "ji1", "ji2", "ji3", "ji4", "ji5", "ji6", "ji7", "[38]","[39]",
                    "[40]", "hana", "hana", "hana", "hana", "hana", "hana", "hana", "hana", "all"];

Deck.numtoname_table =
                   ["[00]", "一萬", "二萬" , "三萬" ,"四萬" ,"五萬" ,"六萬" ,"七萬" ,"八萬" ,"九萬" ,
                    "[10]", "一索", "二索" , "三索" ,"四索" ,"五索" ,"六索" ,"七索" ,"八索" ,"九索" ,
                    "[20]", "一筒", "二筒" , "三筒" ,"四筒" ,"五筒" ,"六筒" ,"七筒" ,"八筒" ,"九筒" ,
                    "[30]", "東" , "南" , "西" , "北" , "發" , "白" , "中" , "[38]","[39]",
                    "[40]", "花", "花", "花", "花", "花", "花", "花", "花", "全" ];

//Deck.numtotile = function(x){ if( x in Deck.numtotile_table ){ return Deck.numtotile_table[x]; }else{ return ""; } };
Deck.numtoname = function(x){ if( x in Deck.numtoname_table ){ return Deck.numtoname_table[x]; }else{ return ""; } };




function* __internal_suit_mentu_kousei(cnt,k,res,part){
  if(k>=15){
    yield res.slice();
    return;
  }
  yield* __internal_suit_mentu_kousei(cnt,k+1,res);
  if( cnt[k] >=3 ){
    cnt[k]-=3;
    res.push([k,k,k].join(","));
    yield* __internal_suit_mentu_kousei(cnt,k,res);
    res.pop();
    cnt[k]+=3;
  }
  if(k<3)return;
  let shun = Math.min(cnt[k],cnt[k-1],cnt[k-2]);
  for(let i=0;i<shun;i++){
    cnt[k]-=1;
    cnt[k-1]-=1;
    cnt[k-2]-=1;
    res.push([k-2,k-1,k].join(","));
    yield* __internal_suit_mentu_kousei(cnt,k+1,res);
  }
  res.splice(-shun,shun);
  cnt[k]+=shun;
  cnt[k-1]+=shun;
  cnt[k-2]+=shun;
}
function __mentu_decoder(suit){
  return function(x){
    return x.map( m => m.split(",").map( q => get_pid(suit,q) ) );
  }
}
function suit_mentu_kousei(suit,x){
  let cnt = new Array(15).fill(0);
  for(let e of x){ cnt[get_number(e)]++; }
  for(let i=0;i<10;i++){
    // TODO 枝刈り
  }
  let all_pat = Array.from(__internal_suit_mentu_kousei(cnt,0,[],[]));
  let max_mentulen = 0;
  let max_mentu = [];
  for(let q of all_pat){
    if(q.length>max_mentulen){
      max_mentulen = q.length;
      max_mentu = [q];
    }else if(q.length == max_mentulen){
      max_mentu.push(q);
    }
  }
  return max_mentu.map(__mentu_decoder(suit));
}
function mentu_kousei(hand,player){
  hand = getsorted(hand);
  let atamaset = new Set();
  let nokori = {};
  for(let k = 0 ; k < hand.length-1;k++){
    if( hand[k] == hand[k+1] && !(atamaset.has(hand[k])) ){
      atamaset.add(hand[k]);
      let cpy = hand.slice();
      cpy.splice(k,2);
      nokori[hand[k]] = cpy;
    }
  }
  let res = [];
  for(var k in nokori){
    k = parseInt(k);
    let grp = grouping(nokori[k],get_suit);
    let grp_kousei = mapeach(suit_mentu_kousei , grp);
    let comb = all_combinations( Object.values( grp_kousei ) );
    //console.log( nokori[k] , grp_kousei );
    for( let c of comb ){
      if( ( c.length + player.exposed.length ) == 4 ){
        res.push( {type:"normal", data:c.concat( [ [k,k] ])} );
      }
    }
  }
  // 特殊系
  if(player.is_menzen()){
    let st = new Set(x);
    // 七対
    {
      let tt = 0;
      let hand_fq = (hand.frequency());
      let kou = [];
      let renzoku = true;
      let lastnum = null;
      for( var k in hand_fq ){
        k = parseInt(k);
        if((hand_fq[k]&1)==0){
          tt+=hand_fq[k];
          kou.push( (new Array(hand_fq[k])).fill(k)  );
          if(hand_fq[k]==2&& ( lastnum == null || k==(lastnum+1) ) ){
            lastnum = k;
          }else{renzoku=false;}
        }else{break;}
      }
      if(tt==14){
        if(renzoku){
          res.push( { type:"ren7pair",data:kou } );
        }else{
          res.push( { type:"7pair",data:kou } );
        }
      }
    }
    // 不靠
    {
      let chars = (new Array(7)).fill(0);
      let numbers = (new Array(9)).fill(0);
      let color = (new Array(3)).fill(null);
      let cnt = 0;
      for( var x in hand ){
        if( 31 <= x && x <= 37 ){
          if(chars[x-31] == 0){
            chars[x-31] = 1;
          }else{break;}
        }else{
          let suit = get_suit_num(x) , num = get_number(x);
          if(color[suit]==null){
            color[suit] = num % 3 ;
          }else{
            if( color[suit] == num % 3 && numbers[num] == 0 ){
              numbers[num] = 1;
            }else{break;}
          }
        }
        cnt++;
      }
      if(cnt==14){
        res.push( { type:"knitted",data:hand } );
      }
    }
    // 国士
    if( st.size == 13 && hand.every( y => set_yaochu.has(y) ) ){
      res.push( { type:"kokushi" } );
    }
  }

  return res;
}

var yaku = [];

function add_yaku( name ,　chinesename ,  value , callback , other ){
  var o = {name:name , chinese_name:chinesename, value:value , callback:callback};
  o = Object.assign( o , other == null ? {} : other  );
  yaku.push( o );
  return o;
}

function construct_yaku(){
  var sorted = [];
  var node = {};
  var input = {};
  for( let v of yaku ){
    input[v.name] = new Set();
  }
  for( let v of yaku ){
    node[v.name] = v;
    if( "override" in v && v.override != null ){
      for( let u of v.override ){
        input[u.name].add(v);
      }
    }else{
      v.override = [];
    }
  }
  let left = yaku.length;
  while( left > 0 ){
    for( let k in yaku ){
      let v = yaku[k];
      if( v.name in input && input[v.name].size == 0 ){
        sorted.push( v );
        for( let u of v.override ){
          input[u.name].delete(v);
        }
        delete input[v.name];
        left--;
      }
    }
  }
  let l = yaku.length;
  for(let i = l-1 ; i>=0 ; i-- ){
    yaku[i].override = Array.prototype.concat.apply(
      yaku[i].override,
      yaku[i].override.map(x=>x.override));
  }
  yaku = sorted;
}

// 実装てきとうスギィ！ 今度改善する
function calc_machi(pl){
  let tiles = [1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,31,32,33,34,35,36,37];
  return tiles.filter( x => {
    let kousei = mentu_kousei( pl.hand.concat(x) , pl );
    return kousei.length > 0 ;
  } );
}

function yakucheck(player,kousei){
  let score = 0;
  let list = [ ];
  let overrided = new Set();
  for( let v of yaku ){
    if(overrided.has(v))continue;
    player.other_data = { kousei_type : kousei.type }
    let r = v.callback(kousei.data,player);
    if(!r)continue;
    if(v.multiple && r > 1){
      score += v.value * r ;
      list.push( { title:v.chinese_name+"x"+r.toString() , score : v.value * r } )
    }else{
      score += v.value ;
      list.push( { title:v.chinese_name , score : v.value } )
    }
    v.override.forEach( x => overrided.add(x));
  }
  return [score,list];
}

var yaku_disp = {score:null,list:null}


// debug importing
/*
function import_hand(str){
  let res = [];


}
*/
