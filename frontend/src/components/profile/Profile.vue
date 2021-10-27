<template>
  <el-container class="profile">
    <el-header>
      <NavigationBar></NavigationBar>
    </el-header>
    <h></h>
    <el-tabs :tab-position="tabPosition">
      <h1>My Profile</h1>
<!--      <template slot-scope="scope">-->
      <el-tab-pane label="My Profile">

            <el-main>
                  <div class="demo-basic--circle" style="margin-left: 5px">
                    <div class="block"><el-avatar :size="100" :src="circleUrl"></el-avatar></div>

                  </div>

                <el-descriptions  column="1">
                  <el-descriptions-item label="username">{{username}}</el-descriptions-item>
                  <el-descriptions-item label="gender">
                    <span v-if="gender===1">Male</span>
                    <span v-else>Female</span>
                  </el-descriptions-item>
                  <el-descriptions-item label="department">{{ department }}</el-descriptions-item>

                  <el-descriptions-item label="E-mail">{{ email }}</el-descriptions-item>
                </el-descriptions>

            </el-main>


          </el-tab-pane>
<!--      </template>-->
    </el-tabs>
  </el-container>
</template>

<script>
import NavigationBar from "@/components/common/NavigationBar";
import axios from "axios";

export default {
  name: "Profile",
  components: {
    NavigationBar,
  },
  data() {
    return {
      // Log In User ID
      user_id: 0,
      username:"unnamed user",
      gender:'',
      department:'',
      email:'',
      tabPosition: 'left',
      circleUrl: "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png",
    };

  },
  mounted: function() {
    // retrieve id of the user who currently logged in
    this.user_id = this.$store.state.uid;
    // load all data, then load the progress panel of the first goal
    Promise.all([this.show()])
  },
  methods: {
    // retrieve all posts data
    show: async function () {
      let url = "http://127.0.0.1:8000/" + "profile/information";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let sent={
        user_id: this.user_id,
        // username: this.user.username
      }
      console.log(this.user_id);
      await axios
          .post(url, JSON.stringify(sent), {
            headers: headers
          })
          .then(response => {
            this.username = response.data.info.username;
            this.gender = response.data.info.gender;
            this.department = response.data.info.department;
            this.email = response.data.info.email;
          });
    }
  }
}
</script>

<style scoped>

</style>
