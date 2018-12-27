<template>
  <div class="yaku-group">
    <table class="yaku-table">
      <thead class="yaku-thead">
        <tr>
          <td class="row-yaku">役</td>
          <td class="row-score">点</td>
        </tr>
      </thead>
			<transition-group tag="tbody" class="yaku-tbody" name="yakuentry">
				<tr v-for="(item,index) in yakus">
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
	data:{
		
	}

};
</script>
<style scoped>

.yakuentry-enter-active{
  animation-name: appear;
	animation-timing-function: ease-in;
  animation-duration: 0.5s;
}
.yakuentry-leave-active{
  animation-name: appear;
	animation-direction: reverse;
	animation-timing-function: ease-out;
  animation-duration: 0.5s;
}

@keyframes appear {
	0% {
		opacity: 0;
		margin-top: -10%;
		margin-left: 50%;
	}
	100% {
		opacity: 100%;
		margin-top: 0%;
		margin-left: 0%;
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