from django.db import models
from django.db.models import F
import learning_forum.const as const
from django.core import serializers


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

    def get_comments_by_pid_transmit(self, pid):
        comments = self.filter(
            post=pid,
            post__status=const.POST_STATUS_PUBLIC
        ).order_by("-created_at").values(
            'id',
            'content',
            'user__first_name',
            'user__last_name',
            'created_at',
        ).annotate(
            cid=F('id'),
            first_name=F('user__first_name'),
            last_name=F('user__last_name'),
        )
        return comments


class Comments(models.Model):
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)
    user = models.ForeignKey('learning_profile.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    content = models.CharField(max_length=300, blank=True, null=True)
    likes = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    objects = CommentsManager()

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'Comments'
        verbose_name_plural = 'Comment'


class Like(models.Model):
    like_type = models.SmallIntegerField()
    user = models.ForeignKey('learning_profile.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)
    comment_id = models.IntegerField(null=True, blank=True)
    like_time = models.DateTimeField()

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'Likes'
        verbose_name_plural = 'Like'
