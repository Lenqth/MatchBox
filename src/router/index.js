import Vue from 'vue'
import Router from 'vue-router'
import Lobby from '@/lobby/lobby'
import Loader from '@/jong/jong'
import MatchRoom from '@/matchroom/matchroom'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Lobby',
      component: Lobby
    },
    {
      path: '/jong',
      name: 'JongLoader',
      component: Loader
    },
    {
      path: '/room',
      name: 'MatchRoom',
      component: MatchRoom
    }
  ]
})
