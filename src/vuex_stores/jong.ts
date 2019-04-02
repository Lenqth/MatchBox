
//参考
//https://qiita.com/tsrnk/items/fd95c3d8013d0795a260
//
import { Mutation, MutationAction, Action, VuexModule, getModule, Module } from "vuex-module-decorators";
import {store} from './root'

@Module({ dynamic: true, store, name: "jong", namespaced: true })
class Jong extends VuexModule {
  prevalent_wind : number = 0;
  wind_offset : number = 0; 

  
 
  @Action({}) 
  async reset(params:Object){

  }

  @Action({}) 
  async expose(params:Object){

  }

  @Action({}) 
  async agari(params:Object){

  }

  

}

export const jongModule = getModule(Jong);