<template>
    <el-container>
<!--  Navigation Bar on the top   -->
      <el-header style="padding-left: 0">
        <NavigationBar class="navigation"></NavigationBar>
      </el-header>

      <el-container v-loading="loading">
<!--   Progress Bar on the left     -->
        <el-aside width=35%>
          <template>
            <div class="progress_panel">
              <!--   User who owns the goal    -->
              <h2> {{goal_user}}'s goal </h2>
              <hr>
              <!--      The dashboard diagram of the progress        -->
              <el-progress type="dashboard" :percentage="progress.percentage" :color="progress.color"></el-progress>
              <br>
              <!--      Description of progress     -->
              <span class="progress">
                {{progress.info}}
              </span>
              <!--      To Do List       -->
              <h2>TODO List</h2>
              <hr>
              <el-table
                  :data="todo"
                  style="width: 100%">
                <el-table-column
                    prop="activity"
                    label="Activity"
                    width="200">
                </el-table-column>
                <el-table-column
                    prop="due"
                    label="Due Date"
                    width="200">
                </el-table-column>
                <el-table-column
                    prop="progress"
                    label="Progress">
                </el-table-column>
              </el-table>
            </div>
          </template>
        </el-aside>

<!--   Posts List     -->
        <el-main >

          <template class="posts">
            <el-table
                :data="posts"
                heigth="250"
                >
              <el-table-column
                  label="Student"
                  width="200">
                <template slot-scope="scope">
                <span style="margin-left: 10px" v-if="scope.row.avatar === ''">
                  <!--    Default Avatar     -->
                  <el-avatar src='https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'></el-avatar>
                </span>
                  <span v-else>
                    <!--    Avatar uploaded by user     -->
                  <el-avatar :src=scope.row.avatar></el-avatar>
                </span>
                  <br>
                  <span class="name">
                  {{scope.row.name}}
                </span>
                  <!--      If user is admin, show a tag        -->
                  <el-tag size="medium" v-if="scope.row.is_admin==1">
                    Admin
                  </el-tag>
                  <br>
                  <!--        Publish Date          -->
                  {{scope.row.date}}
                  <!--        Goal button click to access         -->
                  <el-button size="mini" type="primary" @click="handleGoalClick(scope.row)">Goal</el-button>
                </template>
                <!--  POSTS SECTION    -->
              </el-table-column>
              <el-table-column
                  label="Posts"
                  width="500">
                <template slot-scope="scope">
                  {{scope.row.content}}
                </template>
              </el-table-column>
              <el-table-column label="Operation">
                <template slot-scope="scope">
                  <!--    Like Button    -->
                  <span  v-if="scope.row.liked === 1">
                    <el-button size="mini"
                             @click="handleLike(scope.$index, scope.row)"
                             type="warning" icon="el-icon-star-on"></el-button>
                  </span>
                  <span v-else>
                    <el-button size="mini"
                             @click="handleLike(scope.$index, scope.row)" icon="el-icon-star-off"></el-button>
                  </span>
                  <!--    Comment Button  -->
                  <el-button
                      size="mini"
                      @click="handleComment(scope.$index)" icon="el-icon-chat-dot-round"></el-button>
                  <el-drawer
                      :visible.sync="comments_list"
                      direction="rtl"
                      size="30%">
                    <h2 align="center">Comment List</h2>
                    <p v-if="comments.length===0" align="center">
                      --- No Comments ---
                    </p>
                    <ul>
                      <li v-for="i in comments" :key="i.cid">
                        <span class="name">{{i.commenter}} </span>
                        says:
                        <br>
                        {{i.comment_time}}
                        <hr>
                        &nbsp;&nbsp;
                        {{i.content}}
                        <br>
                        <hr>
                      </li>
                    </ul>
                    <div class="comment-making">
                      <h2>Say something:</h2>
                      <el-input type="textarea" v-model="comment_to_write"
                                :autosize="{ minRows: 2, maxRows: 4}"
                                placeholder="leave your comment here">
                      </el-input>
                      <br>
                      <el-button size="small" type="primary" @click="handleMakeComment()">Comment</el-button>
                    </div>
                  </el-drawer>
                  <!--       Report Button           -->
                  <el-button
                      size="mini"
                      type="danger"
                      @click="handleReport(scope.$index)" icon="el-icon-warning"></el-button>
                  <span v-if="scope.row.uid!==user_id">
                    <!--        No subscription option for my own post            -->
                    <span v-if="scope.row.subscribed===false">
                      <el-button
                          size="mini"
                          type="primary"
                          @click="subscribe(scope.row)">subscribe</el-button>
                    </span>
                    <span v-else>
                      <el-button
                          size="mini"
                          type="primary"
                          @click="unsubscribe(scope.row)">unsubscribe</el-button>
                    </span>
                  </span>
                </template>
              </el-table-column>
            </el-table>
          </template>
        </el-main>
      </el-container>
    </el-container>
</template>


<script>
import axios from "axios";
import NavigationBar from "@/components/common/NavigationBar";

export default {
  name: "Forum",
  props: {
    msg: String
  },
  components: {
    NavigationBar,
  },
  data(){
    return {
      loading: true,
      posts: [],
      todo: [],
      progress: {},
      // Post Panel
      comments_list: false,
      comments: Object,
      count: 0,
      goal_user: "Unnamed User",
      comment_to_write: "",
      pid_to_comment: 0,
      // Log In User ID
      user_id: 0,
    }
  },
  mounted: function() {
    // retrieve id of the user who currently logged in
    this.user_id = this.$store.state.uid;
    // load all data, then load the progress panel of the first goal
    Promise.all([this.show()]).then(()=>
        this.refreshGoal(this.posts[0].pid))
  },
  methods: {
    // retrieve all posts data
    show: async function(){
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
    },
    // access another goal by the post id
    refreshGoal: async function(pid){
      let url = "http://127.0.0.1:8000/" + "forum/retrieve_goal";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let send = {
        uid: this.user_id,
        pid: pid,
      }
      await axios
          .post(url, JSON.stringify(send), {
            headers: headers
          })
          .then(response => {
            this.todo = response.data.todo;
            this.progress.info = response.data.info;
            this.progress.color = response.data.color;
            this.progress.percentage = response.data.percentage;
            this.goal_user = response.data.goal_user;
          });
    },
    // like a post
    handleLike: async function(index, row) {
      row.liked = 1 - (1 * row.liked)

      let url = "http://127.0.0.1:8000/" + "forum/like_post";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let send = {
        post_id: row.pid,
        user_id: this.user_id,
        like: row.liked,
      }
      await axios
          .post(url, JSON.stringify(send), {
            headers: headers
          })
    },
    // checkout the comments of a post
    handleComment: async function(index) {
      this.comments_list = true;
      this.pid_to_comment = this.posts[index].pid;
      let url = "http://127.0.0.1:8000/" + "forum/retrieve_comment";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      await axios
          .post(url, JSON.stringify({
            uid: this.user_id,
            pid:this.posts[index].pid
          }), {
            headers: headers
          })
          .then(response => {
            this.comments = response.data.comments;
          });
    },
    // after a new comment is made, automatically refresh the comment list to display the new one
    refreshComment: async function(){
      let url = "http://127.0.0.1:8000/" + "forum/retrieve_comment";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      await axios
          .post(url, JSON.stringify({
            uid: this.user_id,
            pid:this.pid_to_comment
          }), {
            headers: headers
          })
          .then(response => {
            this.comments = response.data.comments;
          });
    },
    // report a post
    handleReport: function(index) {
      let url = "http://127.0.0.1:8000/" + "forum/report_post";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      axios
          .post(url, JSON.stringify({
            user_id: this.user_id,
            pid: this.posts[index].pid
          }), {
            headers: headers
          })
          .then(response => {
            this.$message({
              message: 'Your report has been successfully received!',
              type: response.data.status,
            });
          });
    },
    // transmitting between the states: liked <-> not liked
    handleCommentLike: async function(row) {
      row.liked = 1 - (1 * row.liked)

      let url = "http://127.0.0.1:8000/" + "forum/like_post";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let send = {
        comment_id: row.cid,
        user_id: this.user_id,
        like: row.liked,
      }
      await axios
          .post(url, JSON.stringify(send), {
            headers: headers
          })
    },
    // click event on the [Goal] button
    handleGoalClick: function(row){
      this.refreshGoal(row.pid)
    },
    // making a new comment, and then refresh the comment list
    handleMakeComment: async function(){
      if (this.comment_to_write.length === 0){
        this.$notify({
          title: 'Warning',
          message: 'Nothing to comment',
          type: 'warning'
        });
        return
      }
      let url = "http://127.0.0.1:8000/" + "forum/write_comment";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let send = {
        user_id: this.user_id,
        pid: this.pid_to_comment,
        content: this.comment_to_write,
      }
      await axios
          .post(url, JSON.stringify(send), {
            headers: headers
          }).then(response => {
            if (response.data.status==="success"){
              this.$notify({
                title: 'Success',
                message: 'Comment created successfully',
                type: 'success'
              });
              this.refreshComment();

            } else {
              this.$notify({
                title: 'Warning',
                message: 'Failed to created your comment',
                type: 'warning'
              });
            }
          })
    },
    subscribe: async function(row){
      let url = "http://127.0.0.1:8000/" + "forum/subscribe_post";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let send = {
        user_id: this.user_id,
        post_id: row.pid,
      }
      await axios
          .post(url, JSON.stringify(send), {
            headers: headers
          }).then(response => {
            if (response.data.status==="success"){
              this.$notify({
                title: 'Success',
                message: response.data.msg,
                type: 'success'
              });
              // Update frontend status
              row.subscribed = false;

            } else {
              this.$notify({
                title: 'Warning',
                message: response.data.msg,
                type: 'warning'
              });
            }
          })
    },
    unsubscribe: async function(row){
      let url = "http://127.0.0.1:8000/" + "forum/unsubscribe_post";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let send = {
        user_id: this.user_id,
        post_id: row.pid,
      }
      await axios
          .post(url, JSON.stringify(send), {
            headers: headers
          }).then(response => {
            if (response.data.status==="success"){
              this.$notify({
                title: 'Success',
                message: response.data.msg,
                type: 'success'
              });
            //  Update frontend status
              row.subscribed = false;
            } else {
              this.$notify({
                title: 'Warning',
                message: response.data.msg,
                type: 'warning'
              });
            }
          })
    },

  }
}
</script>

<style scoped>
.navigation{
  position: fixed;
  /* to ensure that the navigation bar is always at the top & front */
  z-index: 1;
  width: 100%;
  margin-top: -10px;
}
.progress_panel{
  position: fixed;
  margin-left: 40px;
}
.posts{
  width: 100%;
  margin-top: 20px;
  margin-right: 100px;
}
h3 {
  margin: 40px 0 0;
}

li {
  margin: 0 10px;
}
a {
  color: #42b983;
}
el-main{
  margin-left: 100px;
}

.name{
  font-weight: bold;
}

.comment-making{
  margin-left: 20px;
  margin-right: 20px;
  margin-bottom: 10px;
}
</style>