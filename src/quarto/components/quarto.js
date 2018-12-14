

export function item2class(x){
    var res = [];
    if(x==null)return [];
    if( x & 1 ){
      res.push("circle");
    }else{
      res.push("square");
    }
    if( x & 2 ){
      res.push("big");
    }else{
      res.push("small");
    }
    if( x & 4 ){
      res.push("hole");
    }else{
      res.push("nohole");
    }
    if( x & 8 ){
      res.push("black");
    }else{
      res.push("white");
    }
    return res;
  }