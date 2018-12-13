import rxjs from "rxjs";

export function getsorted(x) {
  return x.slice().sort((x, y) => x - y);
}
export function getsorted_rev(x) {
  return x.slice().sort((x, y) => y - x);
}

export function pop_positions(li, positions) {
  let lp = getsorted_rev(positions);
  let res = [];
  for (let k of lp) {
    res.unshift(li.splice(k, 1)[0]);
  }
  return res;
}

class AsyncConnection {
  constructor(sock) {
    this.socket = sock;
    var bf = (this.buffer = []);
    var cb = (this.callbacks = []);
    this.socket.addEventListener("message", function(e) {
      var o = JSON.parse(e.data);
      bf.push(o);
      var rem = [];
      for (var x in cb) {
        if (bf.length > 0) {
          o = bf.shift();
          cb[x](o);
          rem.push(x);
        }
      }
      pop_positions(cb, rem);
    });
  }
}

AsyncConnection.prototype.send = function(obj) {
  // console.log("send",obj);
  this.socket.send(JSON.stringify(obj));
};

AsyncConnection.prototype.receiveAsync = function() {
  if (this.buffer.length > 0) {
    return this.buffer.shift();
  }
  var th = this;
  return new Promise(function(resolve, reject) {
    th.callbacks.push(resolve);
  });
};
