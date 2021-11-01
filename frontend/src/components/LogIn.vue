<template>
  <div class="login-container">
    <el-card class = "info-block">
      <h2>Login</h2>
<!--   Log In Form   -->
      <el-form
          class="login-form"
          :model="model"
          :rules="rules"
          ref="form"
          @submit.native.prevent="login">
<!--    Username Input    -->
        <el-form-item label="Username" prop="username">
          <el-input v-model="model.username" placeholder="Username"></el-input>
        </el-form-item>
<!--    Password Input    -->
        <el-form-item label="Password" prop="password">
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
              class="user-button"
          >Login</el-button><br>
          <!--    Forget Password     -->
        <a class="user-button" @click="forgetPassword">Forgot password</a><br>
<!--    Register    -->
        <a class="user-button" @click="register">Register</a>
        </el-form-item>

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
        username: this.fillBox(),
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
              this.$cookies.set('username', send.username)
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
    },
    // get cookie and fill the input box
    fillBox: function(){
      let cachedData = this.$cookies.get("username");
      if (cachedData == null){
        cachedData = '';
      }
      return cachedData;
    },
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
  background-color: cornflowerblue;
  width: 100%;
  height: 100%;
  border: 2px solid black;
}

.info-block {
  opacity: 1;
  width: 20%;
  height: 60%;
}

.login-form{
  margin-left: 10%;
  margin-right: 10%;
}

.user-button {
	box-shadow:inset 0 1px 0 0 #54a3f7;
  background: #007dc1 linear-gradient(to bottom, #007dc1 5%, #0061a7 100%);
  border-radius:3px;
	border:1px solid #124d77;
	display:inline-block;
	cursor:pointer;
	color:#ffffff;
	font-family:Arial;
	font-size:13px;
  margin: 10px 0 10px 0;
	text-decoration:none;
	text-shadow:0px 1px 0px #154682;
  width: 150px;
  text-align: center;
}
.user-button:hover {
  background: #0061a7 linear-gradient(to bottom, #0061a7 5%, #007dc1 100%);
}
.user-button:active {
	position:relative;
	top:1px;
}

::placeholder {
  color: white;
}

</style>