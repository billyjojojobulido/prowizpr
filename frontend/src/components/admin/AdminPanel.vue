<template>
  <el-container>
    <!--  Navigation Bar on the top   -->
    <el-header>
      <NavigationBar class="navigation"></NavigationBar>
    </el-header>
    <el-aside style="width: 35%">
      <h1>Users Management</h1>
      <ul class="infinite-list" v-infinite-scroll="load" style="overflow:auto">
        <li v-for="i in count" class="infinite-list-item">{{ i }}</li>
      </ul>

    </el-aside>
    <el-main>

    </el-main>
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
  methods:{
    getUsers: async function(){
      let url = "http://127.0.0.1:8000/" + "forum/show";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      await axios
          .post(url, JSON.stringify({user_id: this.user_id}), {
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
</style>