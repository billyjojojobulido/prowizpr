<template>
  <el-container class="profile-container">
<!--  Navigation Bar  -->
    <el-header  style="padding-left: 0; padding-top: 0">
      <NavigationBar class="navigation"></NavigationBar>
    </el-header>
<!--  Make the Tabs on the left side of the page  -->
    <el-tabs :tab-position="tabPosition" v-loading="loading">
<!--  Display Profile Information Page  -->
      <el-tab-pane label="My Profile">
        <h1>My Profile</h1>
        <!--    Display Profile Image    -->
        <el-avatar :size="80" :src=image></el-avatar>
        <el-main>
          <div class="profile-info">
            <!--     Display Personal Information As Form       -->
            <el-descriptions column="1" border size="medium">
              <el-descriptions-item label="First Name">{{profile_form.first_name}}</el-descriptions-item>
              <el-descriptions-item label="Last Name">{{profile_form.last_name}}</el-descriptions-item>
              <el-descriptions-item label="Username">{{profile_form.username}}</el-descriptions-item>
              <el-descriptions-item label="Gender">
                {{genderMap[profile_form.gender]}}
              </el-descriptions-item>
              <el-descriptions-item label="Department">{{ profile_form.department }}</el-descriptions-item>
              <el-descriptions-item label="E-mail">{{ profile_form.email }}</el-descriptions-item>
            </el-descriptions>
          </div>

          <!--    Log Out Button    -->
          <br><br><br><br>
          <el-button
              :loading="loading"
              type="primary"
              block
              @click="logout"
          >Log Out</el-button>
        </el-main>
      </el-tab-pane>

      <!--    Upload Profile Image Tab pane      -->
      <el-tab-pane label="Photo Upload">
        <h1>Photo Upload</h1>
        <!--    Uploader    -->
        <el-upload
            class="avatar-uploader"
            action="https://jsonplaceholder.typicode.com/posts/"
            list-type="picture-card"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload">
          <img v-if="uploadUrl" :src="uploadUrl" class="avatar">
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
        <br>
        <br>
        <div class="avatar-uploader">
          <el-input v-model="uploadUrl"></el-input>
        </div>
        <br>
        <div class="upload-caution">
          <span style="font-weight: bold">Caution:</span>
          Only .jpg or .jpeg files are expected, and the file should not be larger than 2 MB.
        </div>
        <el-button type="primary" icon="el-icon-upload2" @click="upload">Upload</el-button>

<!--     Change Profile Info Tab pane       -->
      </el-tab-pane>

      <!--    Change Profile Information Tab pane      -->
      <el-tab-pane label="Profile Setting">
        <h1>Profile Setting</h1>

        <div class="profile-info">
          <el-descriptions column="1" border size="medium">
            <!--      First Name Input      -->
            <el-descriptions-item label="First Name">
              <el-input :placeholder="profile_form.first_name" v-model="profile_form.first_name"></el-input>
            </el-descriptions-item>
            <!--      Last Name Input      -->
            <el-descriptions-item label="Last Name">
              <el-input :placeholder="profile_form.last_name" v-model="profile_form.last_name"></el-input>
            </el-descriptions-item>
            <!--      Username Section [Not Allowed To Modify]      -->
            <el-descriptions-item label="Username">
              <el-input :placeholder="profile_form.username" v-model="profile_form.username" disabled></el-input>
            </el-descriptions-item>
            <!--      Gender Selection      -->
            <el-descriptions-item label="Gender">
              <el-select v-model="gender">
                <el-option v-for="item in genderOptions"
                           :key="item.value"
                           :label="item.label"
                           :value="item.value">
                </el-option>
              </el-select>
              <!--      Department Input      -->
            </el-descriptions-item>
            <el-descriptions-item label="Department">
              <el-input :placeholder="profile_form.department" v-model="profile_form.department"></el-input>
            </el-descriptions-item>
            <!--      Email Input      -->
            <el-descriptions-item label="E-mail">
              <el-input :placeholder="profile_form.email" v-model="profile_form.email"></el-input>
            </el-descriptions-item>
          </el-descriptions>
        </div>
        <!--    Submit Button    -->
        <br><br><br><br>
        <el-button
            :loading="loading"
            type="primary"
            block
            @click="changeSetting"
        >Save</el-button>
      </el-tab-pane>

<!--     Change Password Tab pane           -->
      <el-tab-pane label="Change Password">
        <h1>Change Password</h1>
        <div class="change-password-form">
          <el-form
              :model="password_model"
              :rules="password_rules"
              ref="form">

            <!--    Old Password Specify    -->
            <el-form-item label="Old Password">
              <el-input v-model="password_model.old_password" placeholder="Old Password" type="password"></el-input>
            </el-form-item>
            <!--    New Password Specify    -->
            <el-form-item label="New Password">
              <el-input v-model="password_model.new_password" placeholder="New Password" type="password"></el-input>
            </el-form-item>
            <!--    Input Password Again to Confirm    -->
            <el-form-item label="Confirm Password">
              <el-input v-model="password_model.new_password_verify" placeholder="Confirm Password" type="password"></el-input>
            </el-form-item>

            <!--    Submit Button    -->
            <el-button
                :loading="loading"
                type="primary"
                block
                @click="changePassword"
            >Submit</el-button>
          </el-form>

        </div>
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
      loading: true,
      user_id: 0,          // Log In User ID
      tabPosition: 'left', // tabs position
      image: "",           // image to display -- My Profile
      uploadUrl: "",       // image uploaded   -- Photo Upload
      gender: "",          // gender - bind to the form
      password_model: {
        old_password: "",
        new_password: "",
        new_password_verify: "",
      }, // password model bind to the form of changing pwd
      password_rules:{
        old_password: [
          {
            required: true,
            message: "You have to enter the old password to authenticate!",
            trigger: "blur"
          },
        ],
        new_password: [
          { required: true,
            message: "New password is required",
            trigger: "blur" },
        ],
        new_password_verify: [
          { required: true,
            message: "You have to type in the password again to verify it",
            trigger: "blur" },
        ],

      }, // password rules of changing pwd
      profile_form: {       // profile model of changing profile information -- Profile Setting
        first_name: "",
        last_name: "",
        username:"unnamed user",
        gender:'',
        department:'',
        email:'',
      },
      genderOptions: [      // gender options allowed -- Profile Setting
        {value:"1", label:"Male"},
        {value:"2", label:"Female"},
        {value:"3", label:"Other Gender"},
      ],
      // Reflecting GenderCode to corresponding text
      genderMap:{
        1: "Male",
        2: "Female",
        3: "Other Gender",
      }
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
      }
      await axios
          .post(url, JSON.stringify(sent), {
            headers: headers
          })
          .then(response => {
            // load all data retrieved into the profile form
            this.profile_form.first_name = response.data.info.first_name;
            this.profile_form.last_name = response.data.info.last_name;
            this.profile_form.username = response.data.info.username;
            this.profile_form.gender = response.data.info.gender;
            this.gender = this.genderMap[response.data.info.gender];
            this.profile_form.department = response.data.info.department;
            this.profile_form.email = response.data.info.email;
            this.image = response.data.info.image;
            this.loading = false;
          });
    },
    logout: async function(){
      // go back to the login page
      await this.$router.push({name:"Login"})
    },
    // handleAvatarSuccess: turn the file uploaded into url
    handleAvatarSuccess(res, file) {
      this.uploadUrl = URL.createObjectURL(file.raw);
    },
    // before upload the file, check if the image file is in jpeg form
    // and the size is less than 2 MB
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg';
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error('Only JPG image is allowed');
      }
      if (!isLt2M) {
        this.$message.error('The image should not exceed 2MB!');
      }
      return isJPG && isLt2M;
    },
    upload: async function(){
      let url = "http://127.0.0.1:8000/" + "profile/upload_image";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let sent={
        user_id: this.user_id,
        url: this.uploadUrl,
      }
      await axios
          .post(url, JSON.stringify(sent), {
            headers: headers
          })
          .then(response => {
            // if upload successfully, then notify the user
            if (response.data.msg === "success"){
              this.$notify({
                title: 'Success',
                message: 'Successfully upload',
                type: 'success'
              });
              // refresh the image loaded in the website
              this.image = this.uploadUrl
            } else {
              this.$notify({
                title: 'Warning',
                message: 'Failed to upload',
                type: 'warning'
              });
            }
          });
    },
    // change the password
    changePassword: async function(){
      let url = "http://127.0.0.1:8000/" + "profile/changepwd";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let sent={
        user_id: this.user_id,
        oldpwd: this.password_model.old_password,
        newpwd: this.password_model.new_password,
      }
      await axios
          .post(url, JSON.stringify(sent), {
            headers: headers
          })
          .then(response => {
            // if changed successfully, then notify the user
            if (response.data.msg === "success"){
              this.$notify({
                title: 'Success',
                message: 'The password has been reset',
                type: 'success'
              });
            } else {
              this.$notify({
                title: 'Warning',
                message: response.data.msg,
                type: 'warning'
              });
            }
          });
    },
    // change the profile basic data
    changeSetting: async function(){
      let url = "http://127.0.0.1:8000/" + "profile/modify_profile";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let sent={
        user_id: this.user_id,
        department: this.profile_form.department,
        gender: this.gender,
        email: this.profile_form.email,
        first_name: this.profile_form.first_name,
        last_name: this.profile_form.last_name,
      }
      await axios
          .post(url, JSON.stringify(sent), {
            headers: headers
          })
          .then(response => {
            // if changed successfully, then notify the user
            if (response.data.msg === "success"){
              this.$notify({
                title: 'Success',
                message: 'The profile has been changed',
                type: 'success'
              });

              this.profile_form.gender = this.gender;
              this.gender = this.genderMap[this.gender];
            } else {
              this.$notify({
                title: 'Warning',
                message: response.data.msg,
                type: 'warning'
              });
            }
          });
    },
  }
}
</script>

<style scoped>
.profile-container{
  background-color: aliceblue;
  width: 100%;
  height: 1000px;
}
.navigation{
  position: fixed;
  /* to ensure that the navigation bar is always at the top & front */
  z-index: 9999;
  width: 100%;
  margin-top: -10px;
}
.profile-info{
  margin-left: 30%;
  margin-right: 30%;
  align-items: center;
  justify-content: center;
}
.avatar-uploader .el-upload {
  cursor: pointer;
  position: relative;
  overflow: hidden;
  justify-content: center;
}
.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}
.avatar-uploader-icon {
  color: #8c939d;
  width: 148px;
  height: 148px;
  line-height: 148px;
  text-align: center;
}
.avatar {
  width: 148px;
  height: 148px;
  display: block;
}
.change-password-form{
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}
</style>
