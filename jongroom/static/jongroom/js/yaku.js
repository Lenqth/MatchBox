
YakuUtil = {}


YakuUtil.debug_set = function(pattern,hand){
  let t = new Set( [ hand.agari_tile , ...hand.hand  , ...( hand.exposed.map( x => x.tiles ).flatten() ) ] );
  return t;
};

// これに含まれる牌のみで作る
YakuUtil.inset = function( _s ){
  let s = new Set(_s);
  return function(pattern,hand){
    let t = new Set( [ hand.agari_tile , ...hand.hand  , ...( hand.exposed.map( x => x.tiles ).flatten() ) ] );
    return t.every(x => s.has(x));
  };
};
// これに含まれる牌を1つ含む
YakuUtil.haveset = function( _s ){
  let s = new Set(_s);
  return function(pattern,hand){
    let t = new Set( [ hand.agari_tile , ...hand.hand  , ...( hand.exposed.map( x => x.tiles ).flatten() ) ] );
    return t.some(x => s.has(x));
  };
};
// これに含まれる牌をそれぞれ1つ含む
YakuUtil.haveallset = function( _s ){
  let s = new Set(_s);
  return function(pattern,hand){
    let t = new Set( [ hand.agari_tile , ...hand.hand  , ...( hand.exposed.map( x => x.tiles ).flatten() ) ] );
    return s.every(x => t.has(x));
  };
};

// これに含まれる牌を含まない
YakuUtil.withoutset = function( _s ){
  let s = new Set(_s);
  return function(pattern,hand){
    let t = new Set( [ hand.agari_tile , ...hand.hand  , ...( hand.exposed.map( x => x.tiles ).flatten() ) ] );
    return t.every(x => !s.has(x));
  };
};
YakuUtil.chows = function( callback ){
  return function(pattern,hand){
    var chows = [];
    chows = chows.concat( hand.exposed.filter( x => x.type == "chow" ).map( x => x.tiles.slice().sortnum() ) ,
            pattern.filter( x=> x[0] != x[1] ).map(x=>x.slice().sortnum()) ) ;
    return callback(chows);
  };
};
YakuUtil.chowbits = function( callback ){
  return function(pattern,hand){
    var bit = 0;
    var heads = [].concat( hand.exposed.filter( x => x.type == "chow" ).map( x => x.tiles.slice().sortnum()[0] ) ,
            pattern.filter( x=> x[0] != x[1] ).map(x=>x.slice().sortnum()[0]) ) ;
    heads.map(b => bit |= 1<<b);
    console.log(heads);
    let mask = (1<<10) - 1;
    return callback(bit&mask,(bit>>10)&mask,(bit>>20)&mask);
  };
};
YakuUtil.pongbits = function( callback ){
  return function(pattern,hand){
    var bit = 0;
    let heads = [].concat( hand.exposed.filter( x => x.type != "chow" ).map( x => x.tiles[0] ) ,
            pattern.filter( x=> x.length >= 3 && x[0] == x[1] ).map(x=>x[0]) ) ;
    heads.map(b => b > 30 ? 0 : (bit |= 1<<b) );
    console.log(heads);
    let mask = (1<<10) - 1;
    return callback(bit&mask,(bit>>10)&mask,(bit>>20)&mask);
  };
};

YakuUtil.colorwise_chows = function( callback ){
  return function(pattern,hand){
    var chows = [];
    chows = chows.concat( hand.exposed.filter( x => x.type == "chow" ).map( x => x.tiles.slice().sortnum() ) ,
            pattern.filter( x=> x[0] != x[1] ).map(x=>x.slice().sortnum()) ) ;
    var suitwise = [ chows.filter(x=>get_suit(x[0])=="MAN") , chows.filter(x=>get_suit(x[0])=="SOU") , chows.filter(x=>get_suit(x[0])=="PIN") ]
    return suitwise.some( callback ) ;
  };
};


YakuUtil.pongs = function( callback ){
  return function(pattern,hand){
    var pongs = [];
    pongs = pongs.concat( hand.exposed.filter( x => x.type != "chow" ).map( x => x.tiles.slice() ) ,
            pattern.filter( x=> x.length >= 3 && x[0] == x[1] ).map(x=>x.slice()) ) ;
    return callback(pongs);
  };
};
YakuUtil.concpongs = function( callback ){
  return function(pattern,hand){
    var pongs = [];
    var tileli = [ hand.agari_tile , ...hand.hand  , ...( hand.exposed.map( x => x.tiles ).flatten() ) ];
    var four = new Set(Object.keys(tileli.frequency().dicfilter( (k,v) => v>=4 )));
    pongs = pongs.concat( hand.exposed.filter( x => x.type == "conckong" ).map( x => x.tiles.slice() ) ,
            pattern.filter( x=> x.length >= 3 && x[0] == x[1] && ( hand.agari_tsumo || hand.agari_tile != x[0] || four.has(x[0]) ) ).map(x=>x.slice()) ) ;
    console.log(four,pongs);
    return callback(pongs);
  };
};

YakuUtil.atama = function( callback ){
  return function(pattern,hand){
    let atama = pattern.filter( x=> x.length == 2 );
    if( atama.length == 1 ){
      return callback(atama[0][0]);
    }else{
      return callback(null);
    }
  };
};

YakuUtil.and = function(){
  var ary = Array.from(arguments);
  return function(pattern,hand){
    return ary.every( f => f(pattern,hand));
  };
}
YakuUtil.or = function(){
  var ary = Array.from(arguments);
  return function(pattern,hand){
    return ary.some( f => f(pattern,hand));
  };
}

YakuUtil.one_color = function( callback ){
  return function(pattern,hand){

  };
}

YakuUtil.machi = function( callback ){
  return function(pattern,hand){

  };
}



/*
                   ["[00]", "一萬", "二萬" , "三萬" ,"四萬" ,"五萬" ,"六萬" ,"七萬" ,"八萬" ,"九萬" ,
                    "[10]", "一索", "二索" , "三索" ,"四索" ,"五索" ,"六索" ,"七索" ,"八索" ,"九索" ,
                    "[20]", "一筒", "二筒" , "三筒" ,"四筒" ,"五筒" ,"六筒" ,"七筒" ,"八筒" ,"九筒" ,
                    "[30]", "東" , "南" , "西" , "北" , "發" , "白" , "中" , "[38]","[39]",
                    "[40]", "花", "花", "花", "花", "花", "花", "花", "花", "全" ];
*/

var set_yaochu = new Set( [1,9,11,19,21,29,31,32,33,34,35,36,37] );
var set_fives = new Set( [5,15,25] );

var machi_tanki = add_yaku("Single Wait","単調将", 2, function(pattern,hand){return hand.machi_single ;});

var twoterms = add_yaku("Two Terminal Chows","老少副",1, YakuUtil.colorwise_chows( function(li){
  var nums = li.map(x=>get_number(x[0]));
  return (nums.indexOf(1)!=-1)&&(nums.indexOf(7)!=-1) }  ));

var pung_t_or_h = add_yaku("Pung Of Terminals/Honors","么九刻",1,YakuUtil.pongs(function(li){
    let s = new Set([1,9,11,19,21,29,31,32,33,34,35,36,37]);
    return li.filter(x=>s.has(x[0])).length;
  } ) ,
  {override:[]} );
var no_honor = add_yaku("No Honor","無字",1, YakuUtil.withoutset( [31,32,33,34,35,36,37] ) );
var all_chows = add_yaku("All Chows","平和",2, YakuUtil.and( YakuUtil.chows( x => x.length == 4 ) , YakuUtil.withoutset( [31,32,33,34,35,36,37] )  ) , { override : [no_honor] } );
var all_simples = add_yaku("All Simples","断么", 2, YakuUtil.inset( [2,3,4,5,6,7,8,12,13,14,15,16,17,18,22,23,24,25,26,27,28] ) , { override : [no_honor] } );
var all_pongs = add_yaku("All Pongs","碰碰和",6, YakuUtil.pongs( function(li){return li.length==4;} ) , {} );

var menzen =  add_yaku("Concealed Hand","門前清", 2, function(pattern,hand){return hand.is_menzen();});
var selfdrawn =  add_yaku("Self Drawn","自摸", 1, function(pattern,hand){return hand.agari_tsumo;});
var menzentsumo =  add_yaku("Fully Concealed","不求人", 4, function(pattern,hand){return hand.is_menzen() && hand.agari_tsumo;} , { override : [menzen,selfdrawn] } );
var allmeld = add_yaku("Melded Hand","全求人", 6, function(pattern,hand){return hand.exposed.filter(x=>x.type!="conckong").length==4 && (!hand.agari_tsumo);} , {override:[machi_tanki]} );

var four = add_yaku("Tile Hog","四帰一",2,function(pattern,hand){
 var tileli = [ hand.agari_tile , ...hand.hand  , ...( hand.exposed.map( x => x.tiles ).flatten() ) ];
 var konged = hand.exposed.filter( x => x.type.indexOf("kong")>=0 ).map(x=>x.tiles[0]);
 return tileli.frequency().dicfilter( (k,v) => v>=4 && konged.indexOf(parseInt(k))==-1 ).length;
} , {multiple:true} );

var outside = add_yaku("Outside Hand","全帯么",4,
  function(pattern,hand){
    let li = [ ...pattern  , ...( hand.exposed.map( x => x.tiles ) ) ] ;
    return li.every(x => x.some( y => set_yaochu.has(y) ) );
  } ,
  {override:[]} );

var all_fives = add_yaku("All Fives","全帯五",16,
  function(pattern,hand){
    let s = new Set([5,15,25]);
    let li = [ ...pattern  , ...( hand.exposed.map( x => x.tiles ) ) ] ;
    return li.every(x => x.some( y => s.has(y) ) );
  } ,
  {override:[]} );

var dragon1 = add_yaku("Dragon Pung","箭刻",2,YakuUtil.pongs(function(li){ return li.filter(x=> 35<=x[0] && x[0]<=37 ).length==1; } ) ,
  {override:[pung_t_or_h]} );
var dragon2 = add_yaku("2 Dragon Pung","双箭刻",6,YakuUtil.pongs(function(li){ return li.filter(x=> 35<=x[0] && x[0]<=37 ).length==2; } ) ,
  {override:[dragon1]} );
var dragon3 = add_yaku("Big Three Dragons","大三元",88,YakuUtil.pongs(function(li){ return li.filter(x=> 35<=x[0] && x[0]<=37 ).length==3; } ) ,
  {override:[dragon2]} );
var dragon3s = add_yaku("Little Three Dragons","小三元",64,
    YakuUtil.and(
      YakuUtil.atama( function(a){ return a!=null && 35<=a && a<=37 } ) ,
      YakuUtil.pongs(function(li){ return li.filter(x=> 35<=x[0] && x[0]<=37 ).length==2; } ) ) ,
  {override:[dragon2]} );

var fieldwind = add_yaku("Prevalent Wind","圏風刻",2,YakuUtil.pongs(function(li){ return li.filter(x=> 31<=x[0] && x[0]<=34 ).length==3; } ) ,
  {override:[]} );
var selfwind = add_yaku("Seat Wind","門風刻",2,YakuUtil.pongs(function(li){ return li.filter(x=> 31<=x[0] && x[0]<=34 ).length==3; } ) ,
  {override:[]} );
var wind3 = add_yaku("Big Three Winds","三風刻",12,YakuUtil.pongs(function(li){ return li.filter(x=> 31<=x[0] && x[0]<=34 ).length==3; } ) ,
  {override:[]} );
var wind4s = add_yaku("Little Four Winds","小四喜",64,
      YakuUtil.and(
        YakuUtil.atama( function(a){ return a!=null && 31<=a && a<=34 } ) ,
        YakuUtil.pongs(function(li){ return li.filter(x=> 31<=x[0] && x[0]<=34 ).length==3; } ) ) ,
    {override:[wind3]} );
var wind4 = add_yaku("Big Four Winds","大四喜",88,YakuUtil.pongs(function(li){ return li.filter(x=> 31<=x[0] && x[0]<=34 ).length==3; } ) ,
  {override:[wind3,fieldwind,selfwind,all_pongs]} );



var onevoid = add_yaku("One Voided Suit","缺一門",1, YakuUtil.or(
  YakuUtil.withoutset( [1,2,3,4,5,6,7,8,9] ) ,
  YakuUtil.withoutset( [11,12,13,14,15,16,17,18,19] ) ,
  YakuUtil.withoutset( [21,22,23,24,25,26,27,28,29] )
) );

var halfflush = add_yaku("Half Flush","混一色",6, YakuUtil.or(
  YakuUtil.inset( [1,2,3,4,5,6,7,8,9,31,32,33,34,35,36,37] ) ,
  YakuUtil.inset( [11,12,13,14,15,16,17,18,19,31,32,33,34,35,36,37] ) ,
  YakuUtil.inset( [21,22,23,24,25,26,27,28,29,31,32,33,34,35,36,37] )
) , { override : [onevoid] } );

var fullflush = add_yaku("Full Flush","清一色",24, YakuUtil.or(
  YakuUtil.inset( [1,2,3,4,5,6,7,8,9] ) ,
  YakuUtil.inset( [11,12,13,14,15,16,17,18,19] ) ,
  YakuUtil.inset( [21,22,23,24,25,26,27,28,29] )
) , { override : [halfflush,no_honor] } );


var alltypes = add_yaku("All Types","五門斉",6, YakuUtil.and(
  YakuUtil.haveset([1,2,3,4,5,6,7,8,9]),
  YakuUtil.haveset([11,12,13,14,15,16,17,18,19]),
  YakuUtil.haveset([21,22,23,24,25,26,27,28,29]),
  YakuUtil.haveset([31,32,33,34]),
  YakuUtil.haveset([35,36,37])
) );

add_yaku("Last Tile","和絶張",4,function(pattern,hand){
  var open_tiles = [];
  for(var p of deck.players){
    open_tiles = open_tiles.concat( p.exposed.map( x => x.tiles ).flatten(), p.trash );
  }
  var type = hand.agari_tile;
  var left_tiles = deck.all_tiles.filter( x => x==type ).length - open_tiles.filter( x => x==type ).length;
  return left_tiles == 1;
} );


add_yaku("Flower","花牌",1, function(pattern,hand){ return hand.pullout.length; } , {bonus : true , multiple:true } );
var chow2m = add_yaku("Mixed Double Chow","喜相逢",1, YakuUtil.chows(function(li){ return li.map( x => get_number(x[0])).frequency().dicfilter( (k,v) => v>=2).length >= 1; })  );
var chow2p = add_yaku("Pure Double Chow","一般高",1, YakuUtil.chows(function(li){ return li.map( x => x[0] ).frequency().dicfilter( (k,v)=> v>=2 ).length; })  , { override : [chow2m] } );
var six = add_yaku("Short Straight","連六",1, YakuUtil.chows(function(li){
    var q = li.map( x => x[0] ).sortnum();
    var prev_suit = null , prev_num = null;
    for( var v of q ){
      let s = get_suit(v) , n = get_number(v);
      if( prev_suit==s && prev_num==(n+3) ){return true;}
      prev_suit=s;
      prev_num=n;
    }
    return false;
  } ) );

var step3p = add_yaku("Three Shifted Chows","一色三歩高",16, YakuUtil.colorwise_chows(function(li){
    var q = li.map( x => x[0] ).sortnum() , qs = new Set(q);
    if(q.length<3)return false;
    return ( qs.has(q[0]+1) && qs.has(q[0]+2) ) || ( qs.has(q[0]+2) && qs.has(q[0]+4) )
        || ( qs.has(q[1]+1) && qs.has(q[1]+2) ) || ( qs.has(q[1]+2) && qs.has(q[1]+4) );
  } ) , {} );

var step4p = add_yaku("Four Shifted Chows","一色四歩高",32, YakuUtil.colorwise_chows(function(li){
    var q = li.map( x => x[0] ).sortnum();
    if(q.length<4)return false;
    return (q[1]!=q[0]) && (q[3]-q[2] == q[2]-q[1]) && (q[2]-q[1] == q[1]-q[0]) ;
  } ) , { override : [step3p,six,twoterms] }  );


var straightp = add_yaku("Pure Straight","清龍",16, YakuUtil.colorwise_chows(function(li){
  if(li.length<3)return false;
  var q = new Set( li.map( x => get_number(x[0]) ) );
  return q.has(1) && q.has(4) && q.has(7);
  } ) , { override : [six,twoterms] } );

var straightm = add_yaku("Mixed Straight","花龍",8, YakuUtil.chows(function(li){
  if(li.length<3)return false;
  let s = new Set([1,4,7,11,14,17,21,24,27]);
  let h = new Set(li.map(x=>x[0]).filter(x=>s.has(x)));
  return ( h.has(1) && ( (h.has(14)&&h.has(27)) || (h.has(17)&&h.has(24)) ) ) ||
         ( h.has(4) && ( (h.has(11)&&h.has(27)) || (h.has(17)&&h.has(21)) ) ) ||
         ( h.has(7) && ( (h.has(11)&&h.has(24)) || (h.has(14)&&h.has(21)) ) );
  } ) , { override : [] } );

// var straightm = add_yaku("Mixed Straight","花龍",8,  , { override : [six,twoterms] } );


var chow3sm = add_yaku("Mixed Triple Chow","三色三同順",8, YakuUtil.chows(function(li){
    var q = new Set(li.map( x => x[0] ));
    for(let i=1;i<=9;i++){
      if( q.has(i) && q.has(10+i) && q.has(20+i) )return true;
    }return false;
  } ) , { override : [chow2m] }  );

var chow3s = add_yaku("Pure Triple Chow","一色三同順",24, YakuUtil.colorwise_chows(function(li){
    var q = li.map( x => x[0] ).sortnum();
    if(q.length<3)return false;
    return q.frequency().dicfilter( (k,v) => v>=3 ).length>=1;
  } ) , { override : [chow2p] }  );
var chow4s = add_yaku("Quadruple Chow","一色四同順",48, YakuUtil.colorwise_chows(function(li){
    var q = li.map( x => x[0] ).sortnum();
    if(q.length<4)return false;
    return q.frequency().dicfilter( (k,v) => v>=4 ).length>=1;
  } ) , { override : [chow3s,four] }  );

var pong2s = add_yaku("Double Pung","双同刻",2, YakuUtil.pongs( function(li){return li.map(x => get_number(x[0])).frequency().dicfilter( (k,v)=>v==2 ).length;} )
  , { override : [] } );
var pong3s = add_yaku("Triple Pung","三同刻",16, YakuUtil.pongs( function(li){return li.map(x => get_number(x[0])).frequency().dicfilter( (k,v)=>v>=3 ).length; } )
  , { override : [pong2s] } );

var pong3sh = add_yaku("Triple Pure Shifted Pungs","一色三節高",24, YakuUtil.pongs( function(li){
  var l = li.map(x=>x[0]).sortnum();
  let prev=null,ren=0;
  for(let x in l){
    if(x==prev+1){
      ren++;
    }else{ren=1;}
    prev=x;
  }
  return ren==3;
} )
  , { override : [] } );

var pong4sh = add_yaku("Four Pure Shifted Pungs","一色四節高",48, YakuUtil.pongs( function(li){
  var l = li.map(x=>x[0]).sortnum();
  let prev=null,ren=0;
  for(let x in l){
    if(x==prev+1){
      ren++;
    }else{ren=1;}
    prev=x;
  }
  return ren==4;
} )
  , { override : [pong2s] } );

var pong2c = add_yaku("2 Concealed Pungs","双暗刻",2, YakuUtil.concpongs( function(li){return li.length==2} )
  , { override : [] } );
var pong3c = add_yaku("3 Concealed Pungs","三暗刻",16, YakuUtil.concpongs( function(li){return li.length==3} )
  , { override : [pong2c] } );
var pong4c = add_yaku("4 Concealed Pungs","四暗刻",64, YakuUtil.concpongs( function(li){return li.length==4} )
  , { override : [pong3c] } );



var kong1 = add_yaku("Melded Kong","明槓", 1, function(pattern,hand){ return hand.exposed.filter(x=>x.type.indexOf("kong")>=0).length>=1; }
  , { override : [] } );
var kong1c = add_yaku("Concealed Kong","暗槓", 2, function(pattern,hand){ return hand.exposed.filter(x=>x.type=="conckong").length>=1; }
  , { override : [kong1] } );
var kong2 = add_yaku("2 Melded Kongs","双明槓", 4, function(pattern,hand){ return hand.exposed.filter(x=>x.type.indexOf("kong")>=0).length>=2; }
  , { override : [kong1] } );
var kong2c = add_yaku("2 Concealed Kongs","双暗槓", 8, function(pattern,hand){ return hand.exposed.filter(x=>x.type=="conckong").length>=2; }
  , { override : [kong2,kong1c,kong1,pong2c] } );
var kong3 = add_yaku("3 Kongs", "三槓",32, function(pattern,hand){ return hand.exposed.filter(x=>x.type.indexOf("kong")>=0).length>=3; }
  , { override : [kong2,kong1] } );
var kong4 = add_yaku("4 Kongs", "四槓",88, function(pattern,hand){ return hand.exposed.filter(x=>x.type.indexOf("kong")>=0).length>=4; }
  , { override : [kong3,kong2,kong1,all_pongs,machi_tanki ] } );



add_yaku("All Even Pungs","全双刻",    24, YakuUtil.and( YakuUtil.inset( [2,4,6,8,12,14,16,18,22,24,26,28] ) , all_pongs.callback ) , { override : [all_simples,all_pongs] }  );

var low4 = add_yaku("Lower Four","小于五",    12, YakuUtil.inset( [1,2,3,4,11,12,13,14,21,22,23,24] ) , { override : [no_honor]} );
var upp4 = add_yaku("Upper Four","大于五",     12, YakuUtil.inset( [6,7,8,9,16,17,18,19,26,27,28,29] ) , { override : [no_honor]} );

add_yaku("All Upper Tiles", "全大",  24, YakuUtil.inset( [7,8,9,17,18,19,27,28,29] ) , { override : [upp4] });
add_yaku("All Middle Tiles", "全中", 24, YakuUtil.inset( [4,5,6,14,15,16,24,25,26] ) , { override : [all_simples] } );
add_yaku("All Lower Tiles","全小",24, YakuUtil.inset( [1,2,3,11,12,13,21,22,23] ) , { override : [low4] });

add_yaku("All Green","緑一色",        88, YakuUtil.inset( [12,13,14,16,18,35] ), { override : [halfflush] } );
add_yaku("Reversible Tiles","推不倒",  8, YakuUtil.inset( [12,14,15,16,18,19,21,22,23,24,25,28,29,36] ), { override : [onevoid] } );

var all_t_or_h = add_yaku("All Terminals/Honors","混么九",32, YakuUtil.inset( [1,9,11,19,21,29,31,32,33,34,35,36,37] ) );
add_yaku("All Honors","字一色",       64, YakuUtil.inset( [31,32,33,34,35,36,37] ) , { override : [all_t_or_h] });
add_yaku("All Terminals","清么九",    64, YakuUtil.inset( [1,9,11,19,21,29] ), { override : [all_t_or_h] } );


add_yaku("Thirteen Orphans","十三么",88,function(pattern,hand){ return hand.other_data.kousei_type == "kokushi"; } , { override : [alltypes,menzen] } );

var sevenpairs = add_yaku("Seven Pairs","七対",24,function(pattern,hand){ return hand.other_data.kousei_type == "7pair"; } , { override : [menzen,machi_tanki] } );
add_yaku("Seven Shifted Pairs","連七対",88,function(pattern,hand){ return hand.other_data.kousei_type == "ren7pair"; } , { override : [sevenpairs] } );

var knitted = add_yaku("Lesser Honors And Knitted Tiles","全不靠",12,function(pattern,hand){ return hand.other_data.kousei_type == "knitted"; } , { override : [alltypes,menzen] } );
add_yaku("Greater Honors And Knitted Tiles","七星不靠",24,function(pattern,hand){
  return hand.other_data.kousei_type == "knitted" && YakuUtil.haveallset([31,32,33,34,35,36,37]); } , { override : [knitted] } );


add_yaku("Last Tile Draw","妙手回春",8,function(pattern,hand){
  return hand.agari_tsumo && deck.array.length==0; } , { override : [selfdrawn] } );


add_yaku("Last Tile Claim","海底撈月",8,function(pattern,hand){
  return (!hand.agari_tsumo) && deck.array.length==0; } , { override : [] } );

add_yaku("Out With Replacement Tile","槓上開花",8,function(pattern,hand){
  return hand.konged; } , { override : [selfdrawn] } );

add_yaku("Robbing The Kongs","搶槓和",8,function(pattern,hand){return hand.chankong; } , { override : [selfdrawn] } );

add_yaku("Three-Suited Terminal Chows","三色双龍会",16, function(pattern,hand){
  let c1 = [],c7 = [],c5=[];
  for( let x of pattern ){
    let y = x.slice().sortnum();
    if(get_suit_num(y[0])>=3)return false;
    if( y.length == 2 && y[0] == y[1] && get_number(y[1]) == 5 ){
      c5 = get_suit_num(y[0]) ;
    }else if( y.length == 3 ){
      if( get_number(y[0]) == 1 && get_number(y[1]) == 2 ){
        c1.push( get_suit_num(y[0]) );
      }else if( get_number(y[0]) == 7 && get_number(y[1]) == 8 ){
        c7.push( get_suit_num(y[0]) );
      }else{return false;}
    }else{
      return false;
    }
  }
  return c1.length == 2 && c7.length == 2 && (new Set([...c1,c5])).size == 3 && (new Set([...c7,c5])).size == 3;
} , { override : [twoterms] } );

add_yaku("Pure Terminal Chows","一色双龍会",64, function(pattern,hand){
  if( !fullflush.callback(pattern,hand) )return false;
  let c1 = 2,c7 = 2;
  for( let x of pattern ){
    let y = x.slice().sortnum();
    if( y.length == 2 && y[0] == y[1] && get_number(y[1]) == 5 ){
    }else if( y.length == 3 ){
      if( get_number(y[0]) == 1 && get_number(y[1]) == 2 ){
        c1--;
      }else if( get_number(y[0]) == 7 && get_number(y[1]) == 8 ){
        c7--;
      }else{return false;}
    }else{
      return false;
    }
  }
  return c1 == 0 && c7 == 0 ;
} , { override : [fullflush,twoterms] } );


add_yaku("Nine Gates","九蓮宝燈",88,function(pattern,hand){
    let h = hand.hand.slice();
    let su = get_suit_num(h[0]);
    if(su >= 3)return false;
    if( h.some( x=> get_suit_num(x) != su  ) ) return false;
    h =  h.map(get_number).sortnum();
    let g = [1,1,1,2,3,4,5,6,7,8,9,9,9];
    for( var k in h){ if( h[k] != g[k] )return false; }
    return su == get_suit_num(hand.agari_tile);
  } , { override : [fullflush,pung_t_or_h,menzen] } );

add_yaku("Mixed Shifted Chows","三色三歩高",6,YakuUtil.chowbits(
  function(a,b,c){
    let q = 0;
    q |= ( a & (b>>1) & (c>>2) );
    q |= ( a & (c>>1) & (b>>2) );
    q |= ( b & (a>>1) & (c>>2) );
    q |= ( b & (c>>1) & (a>>2) );
    q |= ( c & (a>>1) & (b>>2) );
    q |= ( c & (b>>1) & (a>>2) );
    return q != 0;
  }
),
  {override:[]});
add_yaku("Mixed Shifted Pungs","三色三節高",6,YakuUtil.pongbits(
  function(a,b,c){
    let q = 0;
    q |= ( a & (b>>1) & (c>>2) );
    q |= ( a & (c>>1) & (b>>2) );
    q |= ( b & (a>>1) & (c>>2) );
    q |= ( b & (c>>1) & (a>>2) );
    q |= ( c & (a>>1) & (b>>2) );
    q |= ( c & (b>>1) & (a>>2) );
    return q != 0;
  }
),
  {override:[]});

construct_yaku();
