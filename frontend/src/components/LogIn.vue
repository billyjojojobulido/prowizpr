<template>
  <div class="login-container">
    <el-card>
      <h2>Login</h2>
<!--   Log In Form   -->
      <el-form
          class="login-form"
          :model="model"
          :rules="rules"
          ref="form"
          @submit.native.prevent="login">
<!--    Username Input    -->
        <el-form-item prop="username">
          <el-input v-model="model.username" placeholder="Username"></el-input>
        </el-form-item>
<!--    Password Input    -->
        <el-form-item prop="password">
          <el-input
              v-model="model.password"
              placeholder="Password"
              type="password"
          ></el-input>
        </el-form-item>
<!--    Log In Button    -->
        <el-form-item>
          <el-button
              :loading="loading"
              type="primary"
              native-type="submit"
              block
          >Login</el-button>
        </el-form-item>
<!--    Forget Password     -->
        <a class="forgot-password" @click="forgetPassword">Forgot password</a>
        <br>
<!--    Register    -->
        <a class="forgot-password" @click="register">Register</a>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",
  data(){
    return {
      model: {
        username: "",
        password: ""
      },
      loading: false,
      rules: {
        username: [
          {
            required: true,
            message: "Username is required",
            trigger: "blur"
          },
        ],
        password: [
          { required: true, message: "Password is required", trigger: "blur" },
        ]
      }
    }
  },
  methods: {
    // authenticate
    login: async function() {
      let url = "http://127.0.0.1:8000/" + "profile/login";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let send = {
        username: this.model.username,
        password: this.model.password,
      }
      await axios
          .post(url, JSON.stringify(send), {
            headers: headers
          })
          .then(response => {
            if (response.data.status === "success"){
              this.$store.commit('authenticate', response.data.uid);
              this.$store.commit('admin_auth', response.data.is_admin);
              this.$router.push({name: 'Forum'});
            } else {
              this.$notify({
                title: 'Warning',
                message: 'Failed To Log In',
                type: 'warning'
              });
            }
          });
    },
    // go to the forget password page
    forgetPassword: async function(){
      await this.$router.push({name: "ForgetPassword"});
    },
    // go to the register page
    register: async function(){
      await this.$router.push({name: "Register"});
    }
  },
}
</script>

<style scoped>


.login-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: ManropeRegular;
  background-color:  #233142;
  width: 100%;
  height: 1000px;
  border: 2px solid black;
}

::placeholder {
  color: white;
}

</style>