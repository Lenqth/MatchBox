import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Loader from '@/jong/jong'
import MatchRoom from '@/matchroom/matchroom'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
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
