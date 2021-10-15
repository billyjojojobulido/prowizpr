from django.db import models


# Create your models here.
class Goals(models.Model):
    post = models.ForeignKey('learning_forum.Posts', on_delete=models.CASCADE)
    likes = models.IntegerField()
    publish_status = models.IntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'Goals'


class TasksManager(models.Manager):
    def get_tasks_from_gid(self, gid):
        return self.filter(goal_id=gid)


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
