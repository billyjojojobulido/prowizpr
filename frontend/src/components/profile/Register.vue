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

        <el-form-item label="Verification code"  prop="verification_code" >
          <el-row :gutter="10">
            <el-col :div="15" id="code-input">
              <el-input v-model="model.verification_code" placeholder="Verification code"></el-input>
            </el-col>

            <el-col :span="1">
              <el-button type="primary"
                         size="small"
                         @click="send"
                         :disabled="disabled=sendMsgDisabled">
                <span v-if="sendMsgDisabled">{{"please send after "+time}}</span>
                <span v-if="!sendMsgDisabled">Send Verification Code</span></el-button>
            </el-col>
          </el-row>
        </el-form-item>
        <!--    Submit Button    -->
        <el-button
            :loading="loading"
            type="primary"
            block
            @click="submitForm('model');register()"
        >Sign up</el-button>

      </el-form>
    </el-card>

  </div>
</template>

<script>
import axios from "axios";
// import cookies from"vue-cookies"

export default {
  name: "Register",
  data() {
    return {
      time: 60, // 发送验证码倒计时
      sendMsgDisabled: false,
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
      if(this.model.verification_code === ''){
        this.$notify({
          title: 'Warning',
          message: 'Verification code should not be empty',
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
      form.append("verify_code",this.model.verification_code)

      await axios
          .post(url, form,{
            headers: headers
          })
          .then(response => {
            if (response.data.status === "success"){
              this.$notify({
                title: 'Success',
                message: response.data.msg,
                type: 'success'
              });
              this.$router.push({name:"Login"})
            } else {
              this.$notify({
                title: 'Warning',
                message: response.data.msg,
                type: 'warning'
              });
            }
          });

    },
    send: async function () {
      const pattern = /\b[a-z]{4}[0-9]{4}\b/;
      if(pattern.test(this.model.username) === false){
        await this.$alert('Your username format is wrong, please check your username',
            'Failed send', {
              confirmButtonText: 'OK',
            });
        return
      }

      if (this.model.username ===''){
        this.$notify({
          title: 'Warning',
          message: 'There is no user to send code',
          type: 'warning'
        });
        return
      }

      let url = "http://127.0.0.1:8000/" + "profile/reg_email";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let send = {
        username:this.model.username,
        email: this.model.username + "@uni.sydney.edu.au"
      }
      await axios
          .post(url, JSON.stringify(send), {
            headers: headers
          })
          .then(response => {
            if (response.data.status === "success") {
              let me = this;
              me.sendMsgDisabled = true;
              let interval = window.setInterval(function() {
                if ((me.time--) <= 0) {
                  me.time = 60;
                  me.sendMsgDisabled = false;
                  window.clearInterval(interval);
                }
              }, 1000);
              this.$alert('We have sent you a verification code, please check your email inbox',
                  'Successfully send', {
                    confirmButtonText: 'OK',
                  });
              // console.log(this.$cookies.keys())
            } else {
              this.$alert(response.data.msg,
                  'Failed send', {
                    confirmButtonText: 'OK',

                  });
            }
          });
    }
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

#code-input{
  width: 70%;
}

#code-button{
  width: 30%;
}
</style>
