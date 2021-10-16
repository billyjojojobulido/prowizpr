from django.db import models
import learning_forum.const as const

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
        verbose_name_plural = 'Post'


class CommentsManager(models.Manager):
    def get_comments_by_pid(self, pid):
        # TODO banned
        return self.filter(post=pid, post__status=const.POST_STATUS_PUBLIC).order_by("-created_at")


class Comments(models.Model):
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)
    user = models.ForeignKey('learning_profile.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    content = models.CharField(max_length=300, blank=True, null=True)
    objects = CommentsManager()

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'Comments'
        verbose_name_plural = 'Comment'

