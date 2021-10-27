<template>
  <el-container class="profile-container">
    <el-header>
      <NavigationBar></NavigationBar>
    </el-header>
    <el-tabs :tab-position="tabPosition">
      <h1>My Profile</h1>
      <el-tab-pane label="My Profile">
            <el-avatar :size="80" :src=image></el-avatar>

            <el-main>
              <div class="profile-info">
                <el-descriptions column="1" border size="medium">
                  <el-descriptions-item label="First Name">{{first_name}}</el-descriptions-item>
                  <el-descriptions-item label="Last Name">{{last_name}}</el-descriptions-item>
                  <el-descriptions-item label="Username">{{username}}</el-descriptions-item>
                  <el-descriptions-item label="Gender">
                    <span v-if="gender===1">Male</span>
                    <span v-else>Female</span>
                  </el-descriptions-item>
                  <el-descriptions-item label="Department">{{ department }}</el-descriptions-item>

                  <el-descriptions-item label="E-mail">{{ email }}</el-descriptions-item>
                </el-descriptions>
              </div>
              <!--    Submit Button    -->
              <br><br><br><br>
              <el-button
                  :loading="loading"
                  type="primary"
                  block
                  @click="logout"
              >Log Out</el-button>
            </el-main>


          </el-tab-pane>
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
      firstname:"",
      lastname:"",
      gender:'',
      department:'',
      email:'',
      tabPosition: 'left',
      image: "",
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
            this.first_name = response.data.info.first_name;
            this.last_name = response.data.info.last_name;
            this.username = response.data.info.username;
            this.gender = response.data.info.gender;
            this.department = response.data.info.department;
            this.email = response.data.info.email;
            this.image = response.data.info.image;
          });
    },
    logout: async function(){
      await this.$router.push({name:"Login"})
    }
  }
}
</script>

<style scoped>
.profile-container{
  width: 100%;
  height: 1000px;
}
.profile-info{
  margin-left: 30%;
  margin-right: 30%;
  align-items: center;
  justify-content: center;
}
</style>
