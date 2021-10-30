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
                <el-button type="success" @click="restoreUser(scope.$index)">Restore</el-button>
              </span>
            </template>
          </el-table-column>
          <!--    Check Posts    -->
          <el-table-column
              label="Check"
              width="100">
            <el-button icon="el-icon-search" @click="getPosts(row)" circle></el-button>
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
    // load all data, then load the posts management panel of the first user
    this.getUsers()
    Promise.all([this.getUsers()]).then(()=>
        this.getPosts(0))
  },
  methods:{
    // Retrieve all the users that the admin can manage [non-admin users]
    getUsers: async function(){
      let url = "http://127.0.0.1:8000/" + "admins/get_users";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      };
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
      let url = "http://127.0.0.1:8000/" + "admins/ban_user";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      };
      await axios
          .post(url, {user_id:row.uid},{
            headers: headers
          })
          .then(response => {
            if (response.data.status === "success"){
              this.$notify({
                title: 'Success',
                message: 'Banned Successfully',
                type: 'success'
              });
              row.status = "Banned"
            } else {
              this.$notify({
                title: 'Warning',
                message: 'Failed to ban this user',
                type: 'warning'
              });
            }
          });
    },
    // Restore a banned User Account
    restoreUser: async function(row){
      let url = "http://127.0.0.1:8000/" + "admins/restore_user";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      };
      await axios
          .post(url, {user_id:row.uid},{
            headers: headers
          })
          .then(response => {
            if (response.data.status === "success"){
              this.$notify({
                title: 'Success',
                message: 'Restored Successfully',
                type: 'success'
              });
              row.status = "Active"
            } else {
              this.$notify({
                title: 'Warning',
                message: 'Failed to restore this user',
                type: 'warning'
              });
            }
          });
    },
    getPosts: async function(index){
      let url = "http://127.0.0.1:8000/" + "admins/get_posts";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      };
      await axios
          .post(url, {user_id: this.posts[index].uid},{
            headers: headers
          })
          .then(response => {
            this.posts = response.data.posts;
            this.loading = false;
          });
    }
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
  margin-left: 100px;
  width: 100% ;
  justify-content: center;
  text-align: center;
}
</style>