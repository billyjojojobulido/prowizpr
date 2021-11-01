<template>
  <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b">
    <el-menu-item index="0"><i class="el-icon-arrow-left el-icon--left"></i></el-menu-item>
    <el-menu-item index="1">Forum</el-menu-item>
    <el-menu-item index="2">Goal</el-menu-item>
    <el-menu-item index="3">Profile</el-menu-item>
    <el-menu-item index="4" v-if="$store.getters.isAdmin">Admin</el-menu-item>
  </el-menu>

</template>

<script>
export default {
  name: "NavigationBar",
  props: {
    activeIndex: String,
  },
  methods: {
    handleSelect(key){
      if (key === '0'){
        this.$router.push({name:"Login"});
      }
      if (key === '1'){
        this.$router.push({name:"Forum"});
      }
      else if (key === "2"){
        this.$router.push({name:"Goal"});
      }
      else if (key === "3"){
        this.$router.push({name:"Profile"});
      }
      else if (key === "4"){
        this.$router.push({name:"Admin"});
      }
      else {
        this.$router.push("/")
      }
    }

  }
}
</script>

<style scoped>

</style>
