<template>
  <div class="yaku-group">
    <table class="yaku-table">
      <thead class="yaku-thead">
        <tr>
          <td class="row-yaku">役</td>
          <td class="row-score">点</td>
        </tr>
      </thead>
			<transition-group tag="tbody" class="yaku-tbody" name="yakuentry" appear
				@before-enter="beforeEnter"
				@after-enter="afterEnter"
			  @enter-cancelled="afterEnter" > 
				<tr v-for="(item,index) in yakus" :key="item.chinese_name+index" :data-index="index">
					<td>{{item.chinese_name}}</td>
					<td class="alignright">{{item.score}}</td>
				</tr>
			</transition-group>
    </table>
  </div>
</template>
<script>
import Vue from "vue";

export default {
	props:["yakus"],
	methods:{
		beforeEnter(el) {
			console.log(el.dataset.index)
			el.style.opacity = 0;
			let i = parseInt(el.dataset.index, 10)
			el.style.animationDelay = 100 * i + 'ms'
		},
		afterEnter(el) {
			el.style.animationDelay = ''
			el.style.opacity = 1;
		}
	}

};
</script>
<style scoped>
.yakuentry-enter-active{	
  animation-name: appear;
	animation-timing-function: ease-in;
  animation-duration: 0.4s;
	animation-fill-mode: forwards; 
}
.yakuentry-leave-active{
  animation-name: appear;
	animation-direction: reverse;
	animation-timing-function: ease-out;
  animation-duration: 0.4s;
	animation-fill-mode: forwards; 
}

@keyframes appear {
	0% {
		opacity: 0.0;
		transform:translateX(50%);
	}
	1% {
		opacity: 0.0;
		transform:translateX(50%);
	}
	100% {
		opacity: 1.0;
		transform:none;
	}	
}



.yaku-table{
	width:100%;
	margin: auto;
}
.yaku-thead{
	background-color: lightpink;
}
.yaku-tbody{

}
.yaku-tbody>:nth-child(odd){
	background-color: lightgreen;
}
.yaku-tbody>:nth-child(even){
	background-color: lightblue;
}

.row-yaku{
	width:60%;
}
.row-score{
	width:20%;
}
.alignright{
	text-align:right;
	padding-right:5px;
}

</style>