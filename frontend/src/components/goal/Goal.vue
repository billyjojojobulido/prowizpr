<template>
  <el-container class="goal">
    <el-header>
      <h1>My Goal</h1>
    </el-header>
    <el-container v-loading="loading">
      <el-aside width=45%>
        <template>
          <div class="progress_panel">
<!--            <h2> {{goal_user}}'s goal </h2>-->
<!--            <hr>-->
            <el-progress type="dashboard" :percentage="progress.percentage" :color="progress.color"></el-progress>
            <br>
            <span class="progress">
              {{progress.info}}
            </span>
            <h2>TODO List</h2>
            <hr>
            <el-table
                :data="todo"
                style="width: 100%">
              <el-table-column
                  prop="activity"
                  label="Activity"
                  width="170">
              </el-table-column>
              <el-table-column
                  prop="due"
                  label="Due Date"
                  width="95">
              </el-table-column>
              <el-table-column
                  prop="progress"
                  label="Progress"
                  width="600">
                 <template slot-scope="scope">
<!--                <span v-if="scope.row.progress === 1">-->
                  <el-radio-group v-model="scope.row.progress" size="mini">
                    <el-radio-button label="To Do">To Do</el-radio-button>
                    <el-radio-button label="In Progress">in Progress</el-radio-button>
                    <el-radio-button label="Done">Done</el-radio-button>
                  </el-radio-group>
              </template>
              </el-table-column>

            </el-table>
          </div>
        </template>
        <!--Add Task-->
        <el-button type="text" @click="dialogFormVisible1 = true">Add Task</el-button>

        <el-dialog title="Add Task" :visible.sync="dialogFormVisible1">
          <el-form :model="taskForm">
            <el-form-item label="Activity" :label-width="taskFormLabelWidth">
              <el-input v-model="taskForm.task_to_write" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="Due Date" :label-width="taskFormLabelWidth">
              <el-col :span="11">
                <el-date-picker type="date" placeholder="choose date" v-model="taskForm.date1"
                                value-format="yyyy-MM-dd 00:00:00.000000" style="width: 100%;"></el-date-picker>
              </el-col>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible1 = false">Cancel</el-button>
            <el-button type="primary" @click=" handleAddTask(); dialogFormVisible1 = false">OK</el-button>
          </div>
        </el-dialog>
      </el-aside>
      <el-main>

        <template>
          <el-table
              :data="goals"
              heigth="250"
              style="width: 100%">
            <el-table-column
                label="Update time"
                width="150">
              <template slot-scope="scope">
<!--                <span style="margin-left: 10px" v-if="scope.row.avatar === ''">-->
<!--&lt;!&ndash;    Default Avatar     &ndash;&gt;-->
<!--                  <el-avatar src='https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'></el-avatar>-->
<!--                </span>-->
<!--                <span v-else>-->
<!--&lt;!&ndash;    Avatar uploaded by user     &ndash;&gt;-->
<!--                  <el-avatar :src=scope.row.avatar></el-avatar>-->
<!--                </span>-->
<!--                <br>-->
<!--                <span class="name">-->
<!--                  {{scope.row.name}}-->
<!--                </span>-->
<!--                <el-tag size="medium" v-if="scope.row.is_admin==1">-->
<!--                  Admin-->
<!--                </el-tag>-->
<!--                <br>-->
                {{scope.row.date}}
                <el-button size="mini" type="primary" @click="handleGoalClick(scope.row)">Check Goal</el-button>
              </template>
              <!--  POSTS SECTION    -->
            </el-table-column>
            <el-table-column
                label="description"
                width="150">
              <template slot-scope="scope">
                {{scope.row.description}}
<!--                <el-button size="mini" type="primary" @click="handleGoalClick(scope.row)">Check Goal</el-button>-->
              </template>
            </el-table-column>
            <el-table-column label="Likes" width="100">
              <template slot-scope="scope">
                <!--    show likes    -->
                <span  v-if="scope.row.liked === 0">
                  <el-badge :value="0" class = 'item'  type = "primary" size = 'mini'>
                    <i class="el-icon-star-off"></i>
                  </el-badge>
                </span>
                <span v-else>
                  <el-badge :value= "scope.row.liked" class = 'item'  type = "primary" size = 'mini'>
                    <i class="el-icon-star-off" ></i>
                  </el-badge>
                </span>
                 </template>
            </el-table-column>
               <!--  publish status-->
            <el-table-column label="Publish status">
              <template slot-scope="scope">
<!--                <span v-for="r in scope.row">-->
<!--               <span v-if="scope.row.publish_status ===1">-->
                 <el-radio-group v-model="scope.row.publish" size="mini">

                     <el-radio-button label="Publish"></el-radio-button>
                      <el-radio-button label="Private"></el-radio-button>
                  </el-radio-group>
<!--                </span>-->
              </template>
            </el-table-column>
                <!--    choose publish  -->
<!--                <el-button-->
<!--                    size="mini"-->
<!--                    @click="handleComment(scope.$index)" icon="el-icon-chat-dot-round"></el-button>-->
<!--                <el-drawer-->
<!--                    :visible.sync="comments_list"-->
<!--                    direction="rtl"-->
<!--                    size="30%">-->
<!--                  <h2 align="center">Comment List</h2>-->
<!--                  <p v-if="comments.length===0" align="center">-->
<!--                    -&#45;&#45; No Comments -&#45;&#45;-->
<!--                  </p>-->
<!--                  &lt;!&ndash;            <template>&ndash;&gt;-->
<!--                  <ul>-->
<!--                    <li v-for="i in comments" :key="i.cid">-->
<!--                      <span class="name">{{i.commenter}} </span>-->
<!--                      says:-->
<!--                      <br>-->
<!--                      {{i.comment_time}}-->
<!--                      <hr>-->
<!--                      &nbsp;&nbsp;-->
<!--                      {{i.content}}-->
<!--                      <br>-->
<!--                    </li>-->
<!--                    <br>-->
<!--                  </ul>-->
<!--                </el-drawer>-->

          </el-table>
           <!--Add Task-->
        <el-button type="text" @click=" getPosts(); dialogFormVisible2 = true">Add Goal</el-button>

        <el-dialog title="Add Goal" :visible.sync="dialogFormVisible2">
          <el-form :model="goalForm">
            <el-form-item label="Description" :label-width="goalFormLabelWidth">
              <el-input v-model="goalForm.goal_to_write" autocomplete="off"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible2 = false">Cancel</el-button>
            <el-button type="primary" @click=" handleAddGoal(); dialogFormVisible2 = false">OK</el-button>
          </div>
        </el-dialog>
        </template>
      </el-main>
    </el-container>
  </el-container>
</template>



<script>
import axios from "axios";

export default {
  name: "Goal",
  props: {
    msg: String
  },
  data() {
    return {
      goals: [],
      posts: [],
      todo: [],
      progress: {},
      publish: {},
      /*
      * MOCKED
      * */
      user_id: 3,
      dialogFormVisible1: false,
      dialogFormVisible2: false,
      taskForm: {
        task_to_write: '',
        date1: '',
        delivery: false,
        type: [],
      },
      taskFormLabelWidth: '120px',
      goalForm: {
        goal_to_write: '',
        type: [],
      },
      goalFormLabelWidth: '120px',
      // pid_for_add:0
      gid_to_add:0,

    }
  },

  mounted: function () {
    Promise.all([this.show()]).then(() =>
        this.refreshGoal(this.goals[0].gid))
  },
  methods: {

    show: async function () {
      let url = "http://127.0.0.1:8000/" + "goal/show";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      await axios
          .post(url, JSON.stringify({post_id: this.post_id}), {
            headers: headers
          })
          .then(response => {
            this.goals = response.data.goals;
            this.loading = false;
            // this.user_id = response.data.user_id;
            this.publish.info = response.data.info;
          });
    },
    refreshTask: async function (pid) {
      let url = "http://127.0.0.1:8000/" + "goal/retrieve_task";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let send = {
        user_id: this.user_id,
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
            // this.goal_user = response.data.goal_user;
          });
    },
    handleGoalClick: function (row) {
      this.refreshTask(row.gid);
      this.handleTask(row.gid)
    },
    getPosts: async function () {
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
    handleAddGoal: async function () {
      if (this.goalForm.goal_to_write.length === 0) {
        this.$notify({
          title: 'Warning',
          message: 'Nothing to add',
          type: 'warning'
        });
        return
      }
      let url = "http://127.0.0.1:8000/" + "goal/add_goal";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let send = {
        uid: this.user_id,
        pid: this.posts[0].pid + 1,
        description: this.goalForm.goal_to_write,
      }
      await axios
          .post(url, JSON.stringify(send), {
            headers: headers
          }).then(response => {
            if (response.data.status === "success") {
              this.$notify({
                title: 'Success',
                message: 'Goal created successfully',
                type: 'success'
              });
              this.show();

            } else {
              this.$notify({
                title: 'Warning',
                message: 'Failed to add your goal',
                type: 'warning'
              });
            }
          })
    },
    handleAddTask: async function () {
    if (this.taskForm.task_to_write.length === 0 || this.taskForm.date1.length === 0) {
      this.$notify({
        title: 'Warning',
        message: 'Nothing to add',
        type: 'warning'
      });
      return
    }
    let url = "http://127.0.0.1:8000/" + "goal/add_task";
    let headers = {
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    let send = {
      gid: this.gid_to_add,
      description: this.taskForm.task_to_write,
      deadline: this.taskForm.date1
    }
    await axios
        .post(url, JSON.stringify(send), {
          headers: headers
        }).then(response => {
          if (response.data.status === "success") {
            this.$notify({
              title: 'Success',
              message: 'Task created successfully',
              type: 'success'
            });
            this.show();

          } else {
            this.$notify({
              title: 'Warning',
              message: 'Failed to add your tasks',
              type: 'warning'
            });
          }
        })
      },
    handleTask: async function(index) {
      // this.comments_list = true;
      this.gid_to_add = this.posts[index].pid;
      let url = "http://127.0.0.1:8000/" + "forum/retrieve_task";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      await axios
          .post(url, JSON.stringify({
            user_id: this.user_id,
            pid:this.posts[index].pid
          }), {
            headers: headers
          })
          .then(response => {
            this.comments = response.data.comments;
          });
    },
  },



  }
</script>

<style scoped>
.item {
  margin-top: 10px;
  margin-right: 40px;
}
el-main{
  margin-left: 100px;
}

</style>
