<template>
  <div class="register-panel">
    <el-card>
      <h2>Register</h2>
      <el-form
          :model="model"
          :rules="rules"
          class="register-form"
          ref="model">
        <!--    Username Input     -->
        <el-form-item label="Username" prop="username">
          <el-input v-model="model.username" placeholder="Username"></el-input>
        </el-form-item>
        <!--    Password Input    -->
        <el-form-item label="Password" prop="password">
          <el-input v-model="model.password" placeholder="Password" type="password"></el-input>
        </el-form-item>
        <!--    Input Password Again to Confirm    -->
        <el-form-item label="Confirm Password" prop="password_verify">
          <el-input v-model="model.password_verify" placeholder="Confirm Password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="Verification code"  prop="verification_code">
          <el-button type="info" size="mini"
                     @click="open();verify()"
          >Get your Verification code</el-button>
          <el-input v-model="model.verification_code" placeholder="Verification code"></el-input>

        </el-form-item>
        <!--    Submit Button    -->
        <el-button
            :loading="loading"
            type="primary"
            block
            @click="submitForm('model')"
        >Sign up</el-button>

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
        verification_code:'',
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
        verification_code: [
          {required: true,
            message: "Verification code is required",
            trigger: "blur" },
        ]

      },
    };

  },
  methods: {
    open() {
      this.$alert('We have sent you a verification code, please check your email inbox',
          'Successfully send', {
        confirmButtonText: 'OK',
        callback: action => {
          this.$message({
            type: 'info',
            message: `action: ${ action }`
          });
        }
      });
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // this.register();
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
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
      console.assert(this.model.username)
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
    verify: async function (){}
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
