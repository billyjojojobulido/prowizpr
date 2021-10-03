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
        db_table = 'goals'
