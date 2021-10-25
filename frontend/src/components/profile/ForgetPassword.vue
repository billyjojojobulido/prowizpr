<template>
  <div class="forget-password-panel">
    <el-card>
      <h2>Forget Password</h2>
      <el-form
          :model="model"
          :rules="rules"
          class="forget-password-form"
          ref="form">
<!--    Username Input     -->
        <el-form-item label="Username">
          <el-input v-model="model.username" placeholder="Username"></el-input>
        </el-form-item>
<!--    New Password Specify    -->
        <el-form-item label="New Password">
          <el-input v-model="model.new_password" placeholder="New Password" type="password"></el-input>
        </el-form-item>
<!--    Input Password Again to Confirm    -->
        <el-form-item label="Confirm Password">
          <el-input v-model="model.new_password_verify" placeholder="Confirm Password" type="password"></el-input>
        </el-form-item>
<!--    Enter Verification Code after received   -->
        <el-form-item label="Verification Code" class="verification">
          <el-input v-model="model.code" type="text" placeholder="Verification Code"></el-input>
<!--    Click to send verification code via email      -->
          <el-button @click.prevent="sendCode">Send</el-button>
        </el-form-item>
        <!--    Submit Button    -->
        <el-form-item v-if="code_sent===true">
          <el-button
              :loading="loading"
              type="primary"
              block
              @click="change"
          >Submit</el-button>
        </el-form-item>
        <el-form-item v-else>
          <el-button
              :loading="loading"
              type="primary"
              block
              disabled
              @click="change"
          >Submit</el-button>
        </el-form-item>

      </el-form>
    </el-card>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ForgetPassword",
  data() {
    return {
      model:{
        username: "",
        new_password: "",
        new_password_verify: "",
        code: "",
      },
      rules:{
        username: [
          {
            required: true,
            message: "Username is required",
            trigger: "blur"
          },
        ],
        new_password: [
          { required: true,
            message: "Password is required",
            trigger: "blur" },
        ],
        new_password_verify: [
          { required: true,
            message: "You have to type in the password again to verify it",
            trigger: "blur" },
        ],

      },
      code_sent: false,
    };
  },
  methods: {
    sendCode: async function(){
      let url = "http://127.0.0.1:8000/" + "profile/password";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let send = {
        username: this.model.username,
      }
      await axios
          .post(url, JSON.stringify(send), {
            headers: headers
          })
          .then(response => {
            if (response.data.status === "success"){
              this.$notify({
                title: 'Success',
                message: 'Verification Code has been sent! Check your uni email!',
                type: 'success'
              });
              this.code_sent = true;
            } else {
              this.$notify({
                title: 'Warning',
                message: 'Failed to send Verification Code!',
                type: 'warning'
              });
            }
          });
    },
    change: async function (){
      // Verify the two passwords
      if (this.model.new_password !== this.model.new_password_verify){
        this.$notify({
          title: 'Warning',
          message: 'Two passwords do not match!',
          type: 'warning'
        });
        return
      }
      // Send the NEW Password info to the backend
      let url = "http://127.0.0.1:8000/" + "profile/resetpwd";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let send = {
        username: this.model.username,
        password: this.model.new_password,
        code: this.model.code,
      }
      await axios
          .post(url, JSON.stringify(send), {
            headers: headers
          })
          .then(response => {
            if (response.data.status === "success"){
              this.$notify({
                title: 'Success',
                message: 'Password has been changed successfully',
                type: 'success'
              });
              this.$router.push({name:"Login"})
            } else {
              this.$notify({
                title: 'Warning',
                message: 'Failed to Change',
                type: 'warning'
              });
            }
          });

    },
  }
};
</script>

<style scoped>
.forget-password-panel{
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: ManropeRegular;
  background-color:  antiquewhite;
  width: 100%;
  height: 1000px;
  border: 2px solid black;
}

.forget-password-form{
  margin: 10px 100px;
}

.verification{
  display: inline-block;
  position: relative;
}
</style>