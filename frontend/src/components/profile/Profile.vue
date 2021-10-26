<template>
  <el-container class="profile">
    <el-header>
      <NavigationBar></NavigationBar>
    </el-header>
    <h></h>
    <el-tabs :tab-position="tabPosition">
      <el-tab-pane label="My Profile">
        My Profile
            <el-main>
              <el-col :span="4">

                <div class="sub-title"></div>
                <div class="demo-basic--circle">
                  <div class="block"><el-avatar :size="50" :src="circleUrl"></el-avatar></div>
                </div>
              </el-col>

            </el-main>


          </el-tab-pane>


      <el-tab-pane label="Account Security">


      </el-tab-pane>

    </el-tabs>
  </el-container>
</template>

<script>
import NavigationBar from "@/components/common/NavigationBar";
export default {
  name: "Profile",
  components: {
    NavigationBar,
  },
  data() {
    return {
      tabPosition: 'left',
      circleUrl: "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png",

    };
  }
}
</script>

<style scoped>

</style>
