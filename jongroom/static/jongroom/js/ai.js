class AIRandom{
  constructor(hand){
    this.hand = hand;
  }

  get_discard_pos(){
    let hand = this.hand;
    return Math.floor( (hand.hand.length + 1) * Math.random() ) - 1 ;
  }
  claim_check(){
    return false;
  }

}
