from django.db import models


# Create your models here.
class PostsManager(models.Manager):
    def get_all_posts_desc(self):
        posts = self.all().order_by("-created_at")
        return posts


class Posts(models.Model):
    user = models.ForeignKey('learning_profile.User', on_delete=models.CASCADE)
    likes = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    content = models.CharField(max_length=255)
    post_type = models.IntegerField()
    objects = PostsManager()

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'Posts'


class Comments(models.Model):
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)
    user = models.ForeignKey('learning_profile.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    content = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'Comments'