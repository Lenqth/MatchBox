#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
    }
}

#[derive(Default)]
#[derive(Clone)]
struct Tile{
  id:u8
}
impl Tile{
  fn default()->Tile{
    Tile{id:0}
  }
  fn new(id:u8)->Tile{
    Tile{id:id}
  }
  fn get_id(&self) -> u8 {
    self.id % 16
  }
  fn get_suit(&self) -> u8 {
    self.id / 16
  }
  fn copy(&self) -> Tile{
    return Tile{id:self.id}
  }

}

struct Mentu{
  t: u8,
  t1: Tile,
  t2: Tile,
  t3: Tile,
  t4: Tile,
}

impl Mentu{
  pub fn Pong(head:u8) -> Mentu{
    Mentu{t:1,t1:Tile::new(head),t2:Tile::new(head),t3:Tile::new(head),t4:Tile::default()}
  }
  pub fn Chow(head:u8) -> Mentu{
    Mentu{t:2,t1:Tile::new(head),t2:Tile::new(head+1),t3:Tile::new(head+2),t4:Tile::default()}
  }
}

fn shanten( tiles : Vec<Tile> ) -> u8 {
  let mut num_matrix = [ [ 0_i8 ; 16 ] ; 4];
  let mut suit_tiles = [ 0_i8 ; 4 ];
  let mut results = [ [ 0_i8 ; 2 ] ; 4 ];
  for( let tl in tiles ){
    let s = tl.get_suit()
    num_matrix[s][tl.get_id()]++;
    suit_tiles[s]++;
  }
  for( let s in 0..3 ){
    num_matrix[s]
  }


  return 1
}