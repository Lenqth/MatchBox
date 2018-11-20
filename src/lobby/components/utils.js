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
