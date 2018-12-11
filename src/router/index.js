import Vue from 'vue'
import Router from 'vue-router'
import Lobby from '@/lobby/lobby'
import LoaderJong from '@/jong/jong'
import MatchRoom from '@/matchroom/matchroom'

const LoaderD7 = () => import(/* webpackChunkName: "group-foo" */ '@/destiny7/destiny7')

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
      component: LoaderJong
    },
    {
      path: '/destiny7',
      name: 'D7Loader',
      component: LoaderD7
    },
    {
      path: '/room',
      name: 'MatchRoom',
      component: MatchRoom
    }
  ]
})
