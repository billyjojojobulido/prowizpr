from django.db import models


# Create your models here.
class Posts(models.Model):
    user = models.ForeignKey('learning_profile.User', on_delete=models.CASCADE)
    likes = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    content = models.CharField(max_length=255)
    post_type = models.IntegerField()

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'posts'


class Comments(models.Model):
    post = models.ForeignKey('learning_profile.Posts', on_delete=models.CASCADE)
    user = models.ForeignKey('learning_profile.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    content = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'comments'
