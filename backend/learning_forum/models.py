from django.db import models
from django.db.models import F
import learning_forum.const as const
from learning_goal.models import Goals


# Create your models here.
class PostsManager(models.Manager):
    # get posts [admin] - access all posts
    def get_all_posts_desc(self):
        posts = self.all().order_by("-created_at")
        return posts

    # get posts of a user [admin] - access all posts
    def get_posts_by_uid(self, uid):
        posts = self.filter(user=uid).order_by("-report_times")
        return posts

    # ban a post [admin] - clear report times
    def ban_a_post_by_pid(self, pid):
        try:
            post = self.get(pk=pid)
            if post is None:
                return False
            else:
                post.status = const.POST_STATUS_BANNED
                post.report_times = 0
                post.save()
        except Exception as e:
            print(e)
            return False

    # restore a post [admin]
    def restore_a_post_by_pid(self, pid):
        try:
            post = self.get(pk=pid)
            if post is None:
                return False
            else:
                post.status = const.POST_STATUS_PUBLIC
                post.save()
        except Exception as e:
            print(e)
            return False

    # get posts [standard user] - access only standard posts
    def get_all_posts_desc_public(self):
        # User account has to be active and the posts must be sent in public
        posts = self.filter(
            status=const.POST_STATUS_PUBLIC,
            user__is_active=const.USER_ACCOUNT_ACTIVE,
        ).order_by("-created_at")
        return posts

    def report_post(self, pid):
        # report malicious posts
        post = self.get(id=pid)
        post.report_times += 1
        post.save()
        return

    def like_post(self, pid):
        # like the post
        post = self.get(id=pid)
        post.likes += 1
        post.save()
        return

    def dislike_post(self, pid):
        # retract the like sent before
        post = self.get(id=pid)
        post.likes -= 1
        if post.likes < 0:
            post.likes = 0
        post.save()
        return

    def get_full_name_by_pid(self, pid):
        # return the name of the user who sent the post
        post = self.get(id=pid)
        return post.user.first_name, post.user.last_name


class Posts(models.Model):
    user = models.ForeignKey('learning_profile.User', on_delete=models.CASCADE)
    likes = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=255)
    post_type = models.IntegerField()
    report_times = models.IntegerField(default=0)
    objects = PostsManager()

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'Posts'
        verbose_name_plural = 'Post'


class CommentsManager(models.Manager):
    # get comments [admin] - all comments
    def get_all_comments_by_pid(self, pid):
        comments = self.filter(post=pid).order_by("-created_at").values(
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

    # get comments [standard user] - all comments made by Active user accounts under this public post
    def get_comments_by_pid_transmit(self, pid):
        comments = self.filter(
            post=pid,
            post__status=const.POST_STATUS_PUBLIC,
            user__is_active=const.USER_ACCOUNT_ACTIVE,
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

    # write comment [admin & user]
    def write_comment(self, pid, uid, content):
        try:
            self.create(post_id=pid,
                        user_id=uid,
                        content=content)
            return True
        except Exception as e:
            print(e)
            return False


class Comments(models.Model):
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)
    user = models.ForeignKey('learning_profile.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=300, blank=True, null=True)
    likes = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    objects = CommentsManager()

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'Comments'
        verbose_name_plural = 'Comment'


class LikeManager(models.Manager):
    # like a post [admin & user]
    def like_post(self, pid, uid):
        if self.filter(post_id=pid, user_id=uid).count() == 0:
            self.create(
                like_type=const.LIKE_TYPE_POST,
                comment_id=-1,
                post_id=pid,
                user_id=uid,
            )
        Posts.objects.like_post(pid)
        Goals.objects.like_goal(pid)
        return

    # retract a like [admin & user]
    def dislike_post(self, pid, uid):
        try:
            like = self.get(post_id=pid, user_id=uid)
            like.delete()
            Posts.objects.dislike_post(pid)
            Goals.objects.dislike_goal(pid)
            return
        except Exception as e:
            print(e)
            return

    # check whether the post has been liked by a user before [admin / user]
    def check_post_liked(self, pid, uid):
        if self.filter(post_id=pid, user_id=uid).count() > 0:
            return 1
        return 0


class Like(models.Model):
    like_type = models.SmallIntegerField()
    user = models.ForeignKey('learning_profile.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)
    comment_id = models.IntegerField(null=True, blank=True)
    like_time = models.DateTimeField(auto_now=True)
    objects = LikeManager()

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'Likes'
        verbose_name_plural = 'Like'
