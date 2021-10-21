<template>
 <div id="app">
    <el-tabs v-model="activeName" type="card" >
      <el-tab-pane label="Forum" name="first">
        <Forum></Forum>
      </el-tab-pane>
      <el-tab-pane label="My Goal" name="second">
        <Goal></Goal>
      </el-tab-pane>
    </el-tabs>
  </div>
<!--  <div id="app">-->
<!--    <Forum />-->
<!--    <Goal />-->
<!--  </div>-->
</template>

<script>
import Forum from "@/components/forum/Forum";
import Goal from "@/components/goal/Goal";

export default {
  name: 'App',
  components: {
    Forum,
    Goal
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
  background: white;
}
</style>
