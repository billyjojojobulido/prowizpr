from django.db import models


class GoalsManager(models.Manager):
    def get_all_goals_desc(self):
        goals = self.all().order_by("-created_at")
        return goals

    def check_goals_liked(self, pid):
        if self.filter(post_id=pid).count() > 0:
            return 1
        return 0

    def get_full_name(self, gid):
        goal = self.get(pk=gid)
        return goal.post.user.first_name, goal.post.user.last_name

    def add_goal(self, pid, description):
        try:
            self.create(post_id=pid, description=description)
            return True
        except Exception as e:
            print(e)
            return False

    # like a goal
    def like_goal(self, pid):
        # like the post
        goal = self.get(post_id=pid)
        goal.likes += 1
        goal.save()
        return

    # retract the like to the goal
    def dislike_goal(self, pid):
        # retract the like sent before
        goal = self.get(post_id=pid)
        goal.likes -= 1
        if goal.likes < 0:
            goal.likes = 0
        goal.save()
        return


# Create your models here.
class Goals(models.Model):
    post = models.ForeignKey('learning_forum.Posts', on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    publish_status = models.IntegerField(default=1)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GoalsManager()

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'Goals'
        verbose_name_plural = 'Goal'


class TasksManager(models.Manager):
    def get_tasks_from_pid(self, pid):
        return self.filter(goal__post__id=pid)


class Tasks(models.Model):
    goal = models.ForeignKey("Goals", on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    deadline = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TasksManager()

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'Tasks'
        verbose_name_plural = 'Task'
