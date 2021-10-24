<template>
  <div class="login-container">
    <el-card>
      <h2>Login</h2>
      <el-form
          class="login-form"
          :model="model"
          :rules="rules"
          ref="form"
          @submit.native.prevent="login"
      >
        <el-form-item prop="username">
          <el-input v-model="model.username" placeholder="Username"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
              v-model="model.password"
              placeholder="Password"
              type="password"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button
              :loading="loading"
              class="login-button"
              type="primary"
              native-type="submit"
              block
          >Login</el-button>
        </el-form-item>
        <a class="forgot-password" href="https://oxfordinformatics.com/">Forgot password</a>
        <br>
        <a class="forgot-password" href="https://oxfordinformatics.com/">Register</a>
      </el-form>
    </el-card>
  </div>
</template>

<script>
// import axios from "axios";
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
              this.$router.push({name: 'Forum'});
            } else {
              alert("Username and password do not match.")
            }
          });
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
  background-color:  #233142;
  width: 100%;
  height: 700px;
  border: 2px solid black;
}

::placeholder {
  color: white;
}

</style>