import Vue from "vue";
import Router from "vue-router";
import Lobby from "@/lobby/lobby";
import MatchRoom from "@/matchroom/matchroom";
import Sandbox from "@/sandbox/sandbox";

const LoaderJong = () =>
  import(/* webpackChunkName: "group-jong" */ "@/jong/jong");
const LoaderD7 = () =>
  import(/* webpackChunkName: "group-d7" */ "@/destiny7/destiny7");
const LoaderQuarto = () =>
  import(/* webpackChunkName: "group-quarto" */ "@/quarto/index");

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "Lobby",
      component: Lobby
    },
    {
      path: "/room",
      name: "MatchRoom",
      component: MatchRoom
    },
    {
      path: "/jong",
      name: "JongLoader",
      component: LoaderJong
    },
    {
      path: "/destiny7",
      name: "D7Loader",
      component: LoaderD7
    },
    {
      path: "/quarto",
      name: "QuartoLoader",
      component: LoaderQuarto
    },
    {
      path: "/sandbox",
      name: "Sandbox",
      component: Sandbox
    }
  ]
});
