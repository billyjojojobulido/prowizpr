<template>
  <el-container class="goal">
    <el-container>
      <el-header>
        <NavigationBar class="navigation"></NavigationBar>
      </el-header>
      <el-container v-loading="loading">
        <el-aside width=45%>
          <template>
            <div class="progress_panel">
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
                    <el-radio-group v-model="scope.row.progress" size="mini" @change="changeProgressStatus($event,scope.row.tid)">
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
                  <el-radio-group v-model="scope.row.publish" size="mini" @change="changePublishStatus($event,scope.row.gid)">

                    <el-radio-button label="Public" ></el-radio-button>
                    <el-radio-button label="Private" ></el-radio-button>
                  </el-radio-group>
                </template>
              </el-table-column>
            </el-table>
            <!--Add Goal-->
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
  </el-container>
</template>



<script>
import axios from "axios";
import NavigationBar from "@/components/common/NavigationBar";

export default {
  name: "Goal",
  props: {
    msg: String
  },
  components: {
    NavigationBar,
  },
  data() {
    return {
      loading: true,
      goals: [],
      posts: [],
      todo: [],
      progress: {},
      publish: {},
      // Log In User ID
      user_id: 0,
      dialogFormVisible1: false,
      dialogFormVisible2: false,
      taskForm: {
        task_to_write: '',
        date1: '',
        type: [],
      },
      taskFormLabelWidth: '120px',
      goalForm: {
        goal_to_write: '',
        type: [],
      },
      goalFormLabelWidth: '120px',
      gid_to_add:0,
    }
  },

  mounted: function () {
    this.user_id = this.$store.state.uid;
    Promise.all([this.show()]).then(() =>
        this.refreshTask(this.goals[0].gid));
  },

  methods: {
    //change publish status for goal item
    changePublishStatus: async function (e,gid) {
      let url = "http://127.0.0.1:8000/" + "goal/goal_status";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let status=0;
      if (e === "Public") {
        status=1;
      }else if (e ==="Private"){
        status=2;
      }
      let send = {
        status: status,
        goalID: gid,
      }
      await axios
          .post(url, JSON.stringify(send), {
            headers: headers
          })
          .then(response => {
            console.log(response.data.msg) ;
          });

    },
    //change progress status for task item
    changeProgressStatus: async function (e,tid) {
      let url = "http://127.0.0.1:8000/" + "goal/task_status";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let status=0;
      if (e === "To Do") {
        status=1;
      }else if (e ==="In Progress"){
        status=2;
      }else if (e ==="Done"){
        status=3;
      }
      let send = {
        status: status,
        taskID: tid,
        gid:this.gid_to_add
      }
      await axios
          .post(url, JSON.stringify(send), {
            headers: headers
          })
          .then(response => {
            console.log(response.data.msg) ;
            this.refreshTask(this.gid_to_add);

          });

    },
    //show the goals on screen
    show: async function () {
      let url = "http://127.0.0.1:8000/" + "goal/show";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      let send = {
        user: this.user_id,
        post_id: this.post_id
      }
      await axios
          .post(url, JSON.stringify(send), {
            headers: headers
          })
          .then(response => {
            this.goals = response.data.goals;
            this.loading = false;
            this.publish.info = response.data.info;
          });
    },
    // click the check goal button
    handleGoalClick: function (row) {
      this.refreshTask(row.gid);
      this.handleTask(row.gid);
    },
    //refresh the task
    refreshTask: async function (gid) {
      let url = "http://127.0.0.1:8000/" + "goal/retrieve_task";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      this.gid_to_add = gid;
      let send = {
        user_id: this.user_id,
        gid: gid,
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
          });
    },
    //get posts list to check post id
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
    //click add goal button
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
    //access goal id for adding tasks
    handleTask: async function(index) {
      this.gid_to_add = index;

      let url = "http://127.0.0.1:8000/" + "goal/retrieve_task";
      let headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      }
      await axios
          .post(url, JSON.stringify({
            user_id: this.user_id,
            pid:index
          }), {
            headers: headers
          })
          .then(response => {
            this.comments = response.data.comments;
          });
    },
    //click add task button
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
        content: this.taskForm.task_to_write,
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
              this.refreshTask(this.gid_to_add);

            } else {
              this.$notify({
                title: 'Warning',
                message: 'Failed to add your tasks',
                type: 'warning'
              });
            }
          })
    },
  },
  }
</script>

<style scoped>
.goal{
  margin-left: 40px;
  margin-right: 40px;
}
.navigation{
  position: fixed;
  /* to ensure that the navigation bar is always at the top & front */
  z-index: 1;
  width: 100%;
  margin-top: -10px;
}
.item {
  margin-top: 10px;
  margin-right: 40px;
}
el-main{
  margin-left: 100px;
}

</style>
