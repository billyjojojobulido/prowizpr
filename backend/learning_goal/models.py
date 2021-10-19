from django.db import models


class GoalsManager(models.Manager):
    def get_full_name(self, gid):
        goal = self.get(pk=gid)
        return goal.post.user.first_name, goal.post.user.last_name


# Create your models here.
class Goals(models.Model):
    post = models.ForeignKey('learning_forum.Posts', on_delete=models.CASCADE)
    likes = models.IntegerField()
    publish_status = models.IntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
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
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    objects = TasksManager()

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'Tasks'
        verbose_name_plural = 'Task'
