
export function newMethod (o, n, f) {
  Object.defineProperty(o, n, {
    configurable: true,
    enumerable: false,
    value: f
  })
}

export function play_sound (url) {
  url = '@/assets/sound/' + url
  var audio = document.createElement('audio')
  audio.style.display = 'none'
  audio.src = url
  audio.autoplay = true
  audio.onended = function () {
    audio.remove() // Remove when played.
  }
  document.body.appendChild(audio)
}

export function loadJSasync (path) {
  return new Promise((resolve, reject) => {
    let screl = document.createElement('script')
    let done = false
    screl.onload = screl.onreadystatechange = function () {
      if (!done && (!this.readyState ||
                this.readyState === 'loaded' || this.readyState === 'complete')) {
        done = true
        res()
        screl.onload = screl.onreadystatechange = null
        if (screl.parentNode) {
          document.head.removeChild(screl)
        }
      }
    }
    screl.setAttribute('src', path)
    document.head.appendChild(screl)
  })
}

export function taskSleep (ms) {
  return new Promise((resolve) =>
    setTimeout(resolve, ms)
  )
}
var isIterable = function (obj) {
  return obj != null && typeof obj[Symbol.iterator] === 'function'
}
Object.deepClone = function (obj) {
  let res = {}
  for (var name in obj) {
    if (isIterable(obj[name])) {
      r[name] = deepClone(obj[name])
    } else {
      r[name] = obj[name]
    }
  }
  return res
}

export function range (a, b) { var res = []; for (let i = a; i < b; i++) { res.push(i) } return res }

export function benchmark (f, args) {
  let start = performance.now()
  let last = start
  let cnt = 0
  while ((last - start) < 100) {
    f.apply(null, args)
    cnt++
    last = performance.now()
  }
  console.log((last - start) / cnt)
}

export function get_suit (id) {
  var SUIT_NAMES = ['MAN', 'SOU', 'PIN', 'CHAR', 'FLOWER']
  return SUIT_NAMES[Math.floor(id / 10)]
}
export function get_suit_num (id) {
  var SUIT_NAMES = [0, 1, 2, 3, 5]
  return SUIT_NAMES[Math.floor(id / 10)]
}

export function get_number (id) {
  if (id >= 30 && id <= 49) return (id % 10) * 2
  return id % 10
}

export function get_pid (suit, num) {
  let OFFSET = {'MAN': 0, 'SOU': 10, 'PIN': 20, 'CHAR': 30, 'FLOWER': 40}
  let DIV = {'MAN': 1, 'SOU': 1, 'PIN': 1, 'CHAR': 2, 'FLOWER': 2}
  return OFFSET[suit] + Math.floor(num / DIV[suit])
}

export function is_consecutive (ary) {
  let sorted = ary.slice().sort()
  let begin = sorted[0]
  if (begin <= 30) {
    for (let i = 1; i < sorted.length; i++) {
      if (sorted[i] != begin + i) {
        return false
      }
    }
    return true
  } else {
    return false
  }
}

export function shuffle (ary) {
  var res = []
  for (let i = 0; i < ary.length; i++) {
    let r = Math.floor(Math.random() * (i + 1))
    res.push(res[r])
    res[r] = ary[i]
  }
  return res
}

export function mapeach (f, l) {
  res = {}
  for (let k in l) {
    res[k] = f(k, l[k])
  }
  return res
}

export function grouping (l, f) {
  var res = {}
  for (var x of l) {
    let g = f(x)
    if (!(g in res)) {
      res[g] = []
    }
    res[g].push(x)
  }
  return res
}
export function getsorted (x) {
  return x.slice().sort((x, y) => x - y)
}
export function getsorted_rev (x) {
  return x.slice().sort((x, y) => y - x)
}

export function* all_combinations (x, y = []) {
  if (x.length == 0) yield y; else {
    for (let e of x[0]) {
      yield * all_combinations(x.slice(1), y.concat(e))
    }
  }
}

export function take_positions (li, positions) {
  let lp = getsorted_rev(positions)
  let res = []
  for (let k of lp) {
    res.unshift(li.splice(k, 1)[0])
  }
  return res
}

Array.zip = function () {
  var res = []
  var arg = Array.from(arguments)
  var d = arg.length
  var m = Math.min.apply(null, arg.map(x => x.length))
  for (let i = 0; i < m; i++) {
    let tmp = []
    for (let j = 0; j < d; j++) {
      tmp.push(arg[j][i])
    }
    res.push(tmp)
  }
  return res
}
Array.unzip = function (li) {
  var res = []
  var d = li.length
  var m = Math.min.apply(null, li.map(x => x.length))
  for (let i = 0; i < m; i++) {
    let tmp = []
    for (let j = 0; j < d; j++) {
      tmp.push(li[j][i])
    }
    res.push(tmp)
  }
  return res
}

Array.fromRange = function (start, end) {
  return Array(end - start).fill(0).map((v, i) => i + start)
}

export function sort_correspond (li, sortfunc) {
  let target = li.map((k, v) => [k, v])
  target.sort((x, y) => x[0] - y[0])
  return Array.unzip(target)
}

newMethod(Object.prototype, 'dicfilter', function (f) {
  return Object.entries(this).filter(x => f(x[0], x[1]))
})

newMethod(Array.prototype, 'flatten', function () {
  return Array.prototype.concat.apply([], this)
})

newMethod(Array.prototype, 'frequency', function () {
  let res = {}
  for (let v of this) {
    if (v in res) {
      res[v]++
    } else {
      res[v] = 1
    }
  }
  return res
})

newMethod(Set.prototype, 'every', function (f) {
  for (let v of this) {
    if (!f(v)) return false
  }
  return true
})
newMethod(Set.prototype, 'some', function (f) {
  for (let v of this) {
    if (f(v)) return true
  }
  return false
})

newMethod(Array.prototype, 'sortnum', function () { return this.sort((x, y) => x - y) })
