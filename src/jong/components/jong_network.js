
import * as utils from './utils.js'

export class AsyncConnection {
  constructor (sock) {
    this.socket = sock
    var bf = this.buffer = []
    var cb = this.callbacks = []
    this.socket.addEventListener('message', function (e) {
      var o = JSON.parse(e.data)
      bf.push(o)
      var rem = []
      for (var x in cb) {
        if (bf.length > 0) {
          o = bf.shift();
          (cb[x])(o)
          rem.push(x)
        }
      }
      utils.take_positions(cb, rem)
    })
  }
}

AsyncConnection.prototype.send = function (obj) {
  // console.log("send",obj);
  this.socket.send(JSON.stringify(obj))
}

AsyncConnection.prototype.receiveAsync = function () {
  if (this.buffer.length > 0) { return this.buffer.shift() }
  var th = this
  return new Promise(function (resolve) {
    th.callbacks.push(resolve)
  })
}
var Deck = {};
Deck.numtosrc_table =
                   ['back', 'man1', 'man2', 'man3', 'man4', 'man5', 'man6', 'man7', 'man8', 'man9', 'back', 'back', 'back', 'back', 'back', 'back',
                     '[16]', 'pin1', 'pin2', 'pin3', 'pin4', 'pin5', 'pin6', 'pin7', 'pin8', 'pin9', 'back', 'back', 'back', 'back', 'back', 'back',
                     '[32]', 'sou1', 'sou2', 'sou3', 'sou4', 'sou5', 'sou6', 'sou7', 'sou8', 'sou9', 'back', 'back', 'back', 'back', 'back', 'back',
                     '[48]', 'ji1', 'ji2', 'ji3', 'ji4', 'ji5', 'ji6', 'ji7', '[38]', '[39]', 'back', 'back', 'back', 'back', 'back', 'back',
                     '[64]', 'hana', 'hana', 'hana', 'hana', 'hana', 'hana', 'hana', 'hana', 'all', 'back', 'back', 'back', 'back', 'back', 'back']

export class Hand {
  constructor () {
    this.score = 0;
    this.id = -1
    this.hand = []
    this.trash = []
    this.exposed = []
    this.pullout = []
    this.drawed = null
    this.skip_draw = false
    this.konged = false
    this.kousei = null
    this.yakulist = null
    this.yakuscore = null

    this.allow_discard = false
    this.commands_available = []

    this.open = false

    this.target = null
  }
  assign (obj) {
    // hand: Array(13), drew: null, trash: Array(0), exposed: Array(0), flower: 0
    this.hand = obj.hand
    this.drawed = obj.drew
    this.trash = obj.trash
    this.exposed = obj.exposed
    this.flower = obj.flower
    this.score = obj.score
  }
  trash_tile (pos) {
    if (pos == -1) {
      this.drawed = null
    } else {
      this.hand.splice(pos, 1)
      this.hand.push(this.drawed)
      this.drawed = null
    }
    this.hand.sortnum()
  }
}

var _wind_name = ['東', '南', '西', '北']
export function get_wind_name (id) {
  return _wind_name[id]
}


var input_resolve = null

function importAll (r) {
  return r.keys().map(r)
}

const images = importAll(require.context('../assets/', false, /\.(png|jpe?g|svg)$/))

export function numtosrc (x) {
  if (x in Deck.numtosrc_table) {
    return require('@/jong/assets/images30_22/' + Deck.numtosrc_table[x] + '.png')
  } else {
    return ''
  }
}

export function relative_player_format (you, target) {
  var a = ['あなた', '下家', '対面', '上家']
  return a[(((target - you) % 4) + 4) % 4]
}
