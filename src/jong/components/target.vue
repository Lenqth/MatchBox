<template>
  <div class="eff-tgt">
    <div style="transform:rotate(0deg);position:absolute;width:100%;height:100%;top:0px;"><div class="eff-tgt2"></div></div>
    <div style="transform:rotate(90deg);position:absolute;width:100%;height:100%;top:0px;"><div class="eff-tgt2"></div></div>
    <div style="transform:rotate(180deg);position:absolute;width:100%;height:100%;top:0px;"><div class="eff-tgt2"></div></div>
    <div style="transform:rotate(270deg);position:absolute;width:100%;height:100%;top:0px;"><div class="eff-tgt2"></div></div>
  </div>
</template>
<script>
import Vue from 'vue'
export default {}
</script>
<style>
.eff-tgt{
  border: solid 2px orange;
  border-radius: 50%;
  width:32px;
  height:32px;
  position:absolute;
  left:calc(50% - 16px);
  top:calc(50% - 16px);
  animation: spin 1.5s linear infinite;
}
.eff-tgt2{
  z-index:-1;
  position:relative;
  float:left;
  left:calc( 50% - 1px );
  top:-8px;
  width:2px;
  height:15px;
  background:red;
}
@keyframes spin {
  0% {transform: rotate(0deg);}
	100% {transform: rotate(360deg);}
}

</style>
