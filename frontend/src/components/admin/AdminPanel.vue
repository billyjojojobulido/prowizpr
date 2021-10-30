<template>
  <el-container>
    <!--  Navigation Bar on the top   -->
    <el-header>
      <NavigationBar class="navigation"></NavigationBar>
    </el-header>
    <el-container>
      <!--  User Management List : Lists all non-admin users  -->
      <el-aside class="user-management" width="35%">
        <h1>Users Management</h1>
        <el-table
            :data="users">
          <!--   Profile Image    -->
          <el-table-column
              width="100">
            <template slot-scope="scope">
                <span style="margin-left: 10px" v-if="scope.row.avatar === ''">
                  <!--    Default Avatar     -->
                  <el-avatar src='https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'></el-avatar>
                </span>
              <span v-else>
                    <!--    Avatar uploaded by user     -->
                  <el-avatar :src=scope.row.avatar></el-avatar>
                </span>
            </template>

          </el-table-column>
          <!--    User Name      -->
          <el-table-column
              prop="name"
              label="User Name"
              width="150">
          </el-table-column>
          <!--    User Status    -->
          <el-table-column
              prop="status"
              label="Account Status"
              width="150">
          </el-table-column>
          <!--    Operation    -->
          <el-table-column
              label="Operation"
              width="150">

            <template slot-scope="scope">
                <span style="margin-left: 10px" v-if="scope.row.status === 'Active'">
                  <!--        Ban Button          -->
                  <el-button type="danger" @click="banUser(scope.row)">Ban</el-button>
                </span>
              <span v-else>
                    <!--    Restore Button     -->
                <el-button type="success">Restore</el-button>
              </span>
            </template>
          </el-table-column>
        </el-table>

      </el-aside>
      <el-main>

      </el-main>



    </el-container>
  </el-container>

</template>



<script>
// import axios from "axios";
import NavigationBar from "@/components/common/NavigationBar";
import axios from "axios";

export default {
  name: "AdminPanel",
  components:{
    NavigationBar,
  },
  data(){
    return{
      loading: true,
      users: [],
      posts: [],
    }
  },
  mounted: function() {
    // retrieve id of the user who currently logged in
    this.user_id = this.$store.state.uid;
    // load all data, then load the progress panel of the first goal
    this.getUsers()
    // Promise.all([this.getUsers()]).then(()=>
    //     // this.refreshGoal(this.posts[0].pid))
    //     alert("haha"))
  },
  methods:{
    // Retrieve all the users that the admin can manage [non-admin users]
    getUsers: async function(){
      let url = "http://127.0.0.1:8000/" + "admins/get_users";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      await axios
          .get(url, {
            headers: headers
          })
          .then(response => {
            this.users= response.data.users;
            this.loading = false;
          });
    },

    // Ban an active User Account
    banUser: async function(row){
      let url = "http://127.0.0.1:8000/" + "admins/get_users";
    },

  }
}
</script>

<style scoped>
.navigation{
  position: fixed;
  margin-left: 40px;
  margin-right: 40px;
  /* to ensure that the navigation bar is always at the top & front */
  z-index: 9999;
  width: 100%;
  margin-top: -10px;
}
.user-management{
  margin-left: 50px;
  width: 100% ;
  justify-content: center;
  text-align: center;
}
</style>