<template>
  <div class="register-panel">
    <el-card>
      <h2>Register</h2>
      <el-form
          :model="model"
          :rules="rules"
          class="register-form"
          ref="form">
        <!--    Username Input     -->
        <el-form-item label="Username">
          <el-input v-model="model.username" placeholder="Username"></el-input>
        </el-form-item>
        <!--    Password Input    -->
        <el-form-item label="Password">
          <el-input v-model="model.password" placeholder="Password" type="password"></el-input>
        </el-form-item>
        <!--    Input Password Again to Confirm    -->
        <el-form-item label="Confirm Password">
          <el-input v-model="model.password_verify" placeholder="Confirm Password" type="password"></el-input>
        </el-form-item>
        <!--    Submit Button    -->
        <el-button
            :loading="loading"
            type="primary"
            block
            @click="register"
        >Sign Up</el-button>

      </el-form>
    </el-card>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Register",
  data() {
    return {
      model:{
        username: "",
        password: "",
        password_verify: "",
      },
      rules:{
        username: [
          {
            required: true,
            message: "Username is required",
            trigger: "blur"
          },
        ],
        password: [
          { required: true,
            message: "Password is required",
            trigger: "blur" },
        ],
        password_verify: [
          { required: true,
            message: "You have to type in the password again to verify it",
            trigger: "blur" },
        ],

      },
    };
  },
  methods: {
    register: async function (){
      // Verify the two passwords
      if (this.model.password !== this.model.password_verify){
        this.$notify({
          title: 'Warning',
          message: 'Two passwords do not match!',
          type: 'warning'
        });
        return
      }
      // Send the Sign Up request to the backend
      let url = "http://127.0.0.1:8000/" + "profile/register";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let form = new FormData()
      form.append("username", this.model.username)
      form.append("email", this.model.username + "@uni.sydney.edu.au")
      form.append("password1", this.model.password)
      form.append("password2", this.model.password_verify)

      await axios
          .post(url, form, {
            headers: headers
          })
          .then(response => {
            if (response.data.status === "success"){
              this.$notify({
                title: 'Success',
                message: 'Registered Successfully',
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
.register-panel{
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

.register-form{
  margin: 10px 100px;
}

.verification{
  display: inline-block;
  position: relative;
}
</style>