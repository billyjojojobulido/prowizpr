from datetime import datetime
from unittest import TestCase as UnitTestCase
import pytz
from django.test import TestCase, RequestFactory
from learning_goal.models import Goals
from .views import *


# TEST Helper functions
class TestForumUtils(UnitTestCase):

    def setUp(self):
        self.tz = pytz.timezone("Asia/Shanghai")  # unite time zone

    def test_color_percentage(self):
        color_1 = utils.get_color(0)
        self.assertEqual("#f56c6c", color_1)
        color_2 = utils.get_color(20)
        self.assertEqual("#e6a23c", color_2)
        color_3 = utils.get_color(40)
        self.assertEqual("#5cb87a", color_3)
        color_4 = utils.get_color(60)
        self.assertEqual("#1989fa", color_4)
        color_5 = utils.get_color(80)
        self.assertEqual("#6f7ad3", color_5)
        color_6 = utils.get_color(100)
        self.assertEqual("#6f7ad3", color_6)

    def test_color_out_of_range(self):
        color_nak = utils.get_color(-100)
        self.assertEqual("#f56c6c", color_nak)
        color_min = utils.get_color(0)
        self.assertEqual("#f56c6c", color_min)
        color_max = utils.get_color(100)
        self.assertEqual("#6f7ad3", color_max)
        color_sur = utils.get_color(1000)
        self.assertEqual("#6f7ad3", color_sur)

    def test_time_format(self):
        timestamp = 1462451334
        date_time = datetime.fromtimestamp(timestamp, tz=self.tz)
        time_format = "2016-05-05 20:28:54"
        # might result in a problem: localtime -> running in different time zone
        self.assertEqual(utils.time_format(date_time), time_format)

    def test_date_format(self):
        timestamp = 1462451334
        date_time = datetime.fromtimestamp(timestamp)
        time_format = "2016-05-05"
        # might result in a problem: localtime -> running in different time zone
        self.assertEqual(utils.date_format(date_time), time_format)

    def test_empty_check(self):
        self.assertTrue(utils.check_str_empty(""))
        self.assertTrue(utils.check_str_empty(None))
        self.assertFalse(utils.check_str_empty("a"))

    def test_invalid_full_name(self):
        self.assertEqual(utils.get_full_name(None, None), "Unnamed User")
        self.assertEqual(utils.get_full_name("", None), "Unnamed User")
        self.assertEqual(utils.get_full_name(None, ""), "Unnamed User")
        self.assertEqual(utils.get_full_name("", ""), "Unnamed User")

    def test_first_name(self):
        self.assertEqual(utils.get_full_name("Billy", None), "Billy")
        self.assertEqual(utils.get_full_name("Billy", ""), "Billy")

    def test_last_name(self):
        self.assertEqual(utils.get_full_name(None, "Wong"), "Wong")
        self.assertEqual(utils.get_full_name("", "Wong"), "Wong")

    def test_full_name(self):
        self.assertEqual(utils.get_full_name("Billy", "Wong"), "Billy Wong")

    def test_invalid_status(self):
        self.assertEqual(utils.get_progress_msg(0), "Invalid Task Progress")
        self.assertEqual(utils.get_progress_msg(-10), "Invalid Task Progress")
        self.assertEqual(utils.get_progress_msg(1000), "Invalid Task Progress")

    def test_status_msg(self):
        self.assertEqual(utils.get_progress_msg(1), "To Do")
        self.assertEqual(utils.get_progress_msg(2), "In Progress")
        self.assertEqual(utils.get_progress_msg(3), "Done")

    def test_publish_msg(self):
        self.assertEqual(utils.get_publish_msg(1), "Public")
        self.assertEqual(utils.get_publish_msg(2), "Private")


class TestForumModels(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username="test1234",
            password="1234",
            email="test1234@gmail.com",
            first_name="Unit",
            last_name="Testing",
            is_superuser=False,
            is_active=True,
        )
        self.banned_user = User.objects.create(
            username="test5678",
            password="1234",
            email="test5678@gmail.com",
            first_name="Regression",
            last_name="Testing",
            is_superuser=False,
            is_active=False,
        )
        self.post = Posts.objects.create(
            user_id=self.user.id,
            content="How you like that",
            status=1,
            active=1,
            likes=0,
            post_type=1,
        )
        self.private_post = Posts.objects.create(
            user_id=self.user.id,
            content="We dont talk anymore",
            status=2,
            active=1,
            likes=10,
            post_type=1,
        )
        self.comment = Comments.objects.create(
            user_id=self.user.id,
            post_id=self.post.id,
            content="Hello World",
            status=1,
            likes=0,
        )
        self.another_comment = Comments.objects.create(
            user_id=self.banned_user.id,
            post_id=self.post.id,
            content="Goodbye World",
            status=1,
            likes=0,
        )
        self.goal = Goals.objects.create(
            likes=0,
            publish_status=1,
            description="Something",
            post_id=self.post.id,
        )

    def test_show(self):
        payload = {
            "user_id": self.user.id,
        }
        request = self.factory.post(
            '/forum/show',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = show(request)
        content = json.loads(response.content.decode())
        self.assertEqual(len(content['posts']), 1)
        self.assertEqual(response.status_code, 200)

    # TEST Feature: Users can access other's goal

    def test_retrieve_goal(self):
        payload = {
            "pid": self.post.id,
        }
        request = self.factory.post(
            '/forum/retrieve_goal',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = retrieve_goal(request)
        content = json.loads(response.content.decode())
        self.assertEqual(len(content['todo']), 0)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_comment(self):
        payload = {
            "pid": self.post.id,
            "uid": self.user.id,
        }
        request = self.factory.post(
            '/forum/retrieve_comment',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = retrieve_comment(request)
        content = json.loads(response.content.decode())
        self.assertEqual(len(content['comments']), 1)
        self.assertEqual(response.status_code, 200)

    # TEST Feature: report malicious post

    def test_report_post(self):
        payload = {
            "pid": self.post.id,
        }
        request = self.factory.post(
            '/forum/report_post',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = report_post(request)
        post = Posts.objects.get(id=self.post.id)
        self.assertEqual(post.report_times, 1)
        self.assertEqual(response.status_code, 200)

    # TEST Feature: commenting

    def test_write_comment(self):
        payload = {
            "user_id": self.user.id,
            "pid": self.post.id,
            "content": "Hello World",
        }
        request = self.factory.post(
            '/forum/write_comment',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = write_comment(request)
        comments = Comments.objects.filter(user_id=self.user.id, post_id=self.post.id)
        self.assertEqual(len(comments), 2)
        self.assertEqual(response.status_code, 200)

    # TEST Feature: liking

    def test_like_post(self):
        payload = {
            "user_id": self.user.id,
            "post_id": self.post.id,
            "like": 1,
        }
        request = self.factory.post(
            '/forum/like_post',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = like_post(request)
        post = Posts.objects.get(id=self.post.id)
        self.assertEqual(post.likes, 1)
        self.assertEqual(response.status_code, 200)

    def test_dislike_post(self):
        payload = {
            "user_id": self.user.id,
            "post_id": self.post.id,
            "like": 0,
        }
        request = self.factory.post(
            '/forum/like_post',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = like_post(request)
        post = Posts.objects.get(id=self.post.id)
        self.assertEqual(post.likes, 0)
        self.assertEqual(Like.objects.count(), 0)
        self.assertEqual(response.status_code, 200)

    # TEST Feature: subscribing post

    def test_subscribe(self):
        payload = {
            "user_id": self.user.id,
            "post_id": self.post.id,
        }
        request = self.factory.post(
            '/forum/subscribe_post',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = subscribe_post(request)
        subscribes = Subscription.objects.filter(user_id=self.user.id, post_id=self.post.id)
        self.assertEqual(len(subscribes), 1)
        self.assertEqual(response.status_code, 200)

    def test_unsubscribe(self):
        payload = {
            "user_id": self.user.id,
            "post_id": self.post.id,
        }
        request = self.factory.post(
            '/forum/unsubscribe_post',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = unsubscribe_post(request)
        subscribes = Subscription.objects.filter(user_id=self.user.id, post_id=self.post.id)
        self.assertEqual(len(subscribes), 0)
        self.assertEqual(response.status_code, 200)

    # TESTING ORM FUNCTIONS

    def test_retrieve_posts_desc_length(self):
        posts = Posts.objects.get_all_posts_desc()
        self.assertEqual(len(posts), 2)

    def test_retrieve_posts_public_desc_length(self):
        posts = Posts.objects.get_all_posts_desc_public()
        self.assertEqual(len(posts), 1)

    def test_get_post_by_uid(self):
        posts = Posts.objects.get_posts_by_uid(self.user.id)
        self.assertEqual(len(posts), 2)

    def test_get_post_by_uid_false(self):
        posts = Posts.objects.get_posts_by_uid(0)
        self.assertEqual(len(posts), 0)

    def test_ban_post(self):
        Posts.objects.ban_a_post_by_pid(self.post.id)
        post = Posts.objects.get(pk=self.post.id)
        self.assertFalse(post.active)

    def test_ban_not_exist(self):
        self.assertFalse(Posts.objects.ban_a_post_by_pid(0))

    def test_ban_invalid_param(self):
        self.assertFalse(Posts.objects.ban_a_post_by_pid("0"))

    def test_unban_post(self):
        Posts.objects.ban_a_post_by_pid(self.post.id)
        Posts.objects.restore_a_post_by_pid(self.post.id)
        post = Posts.objects.get(pk=self.post.id)
        self.assertTrue(post.active)

    def test_unban_post_not_exist(self):
        self.assertFalse(Posts.objects.restore_a_post_by_pid(0))

    def test_unban_post_invalid_param(self):
        self.assertFalse(Posts.objects.restore_a_post_by_pid("0"))

    def test_report_post_orm(self):
        Posts.objects.report_post(self.post.id)
        post = Posts.objects.get(pk=self.post.id)
        self.assertEqual(post.report_times, 1)

    def test_report_clear_after_ban(self):
        Posts.objects.report_post(self.post.id)
        Posts.objects.ban_a_post_by_pid(self.post.id)
        post = Posts.objects.get(pk=self.post.id)
        self.assertEqual(post.report_times, 0)

    def test_like_post_orm(self):
        Posts.objects.like_post(self.post.id)
        post = Posts.objects.get(pk=self.post.id)
        self.assertEqual(post.likes, 1)

    def test_dislike_post_orm(self):
        Posts.objects.like_post(self.post.id)
        Posts.objects.dislike_post(self.post.id)
        post = Posts.objects.get(pk=self.post.id)
        self.assertEqual(post.likes, 0)

    def test_dislike_post_below_zero(self):
        Posts.objects.dislike_post(self.post.id)
        post = Posts.objects.get(pk=self.post.id)
        self.assertEqual(post.likes, 0)

    def test_get_full_name_by_pid(self):
        first_name, last_name = Posts.objects.get_full_name_by_pid(self.post.id)
        self.assertEqual(first_name, "Unit")
        self.assertEqual(last_name, "Testing")

    def test_get_all_comments_by_pid(self):
        comments = Comments.objects.get_all_comments_by_pid(self.post.id)
        self.assertEqual(len(comments), 2)

    def test_get_all_comments_by_invalid_pid(self):
        comments = Comments.objects.get_all_comments_by_pid(0)
        self.assertEqual(len(comments), 0)

    def test_get_comments_by_pid(self):
        comments = Comments.objects.get_comments_by_pid_transmit(self.post.id)
        self.assertEqual(len(comments), 1)

    def test_get_comments_by_pid_invalid(self):
        comments = Comments.objects.get_comments_by_pid_transmit(0)
        self.assertEqual(len(comments), 0)

    def test_write_comment_orm(self):
        self.assertTrue(Comments.objects.write_comment(self.post.id, self.user.id, "Test Comment"))

    def test_like_post_orm_2(self):
        Like.objects.like_post(self.post.id, self.user.id)
        likes = Like.objects.filter(post_id=self.post.id, user_id=self.user.id)
        self.assertEqual(likes.count(), 1)

    def test_dislike_post_orm_2(self):
        Like.objects.like_post(self.post.id, self.user.id)
        Like.objects.dislike_post(self.post.id, self.user.id)
        likes = Like.objects.filter(post_id=self.post.id, user_id=self.user.id)
        self.assertEqual(likes.count(), 0)

    def test_checked_post_liked_positive(self):
        Like.objects.like_post(self.post.id, self.user.id)
        self.assertEqual(Like.objects.check_post_liked(self.post.id, self.user.id), 1)

    def test_checked_post_liked_negative(self):
        self.assertEqual(Like.objects.check_post_liked(self.post.id, self.user.id), 0)

    def test_is_subscribed_negative(self):
        self.assertFalse(Subscription.objects.is_subscribed(self.post.id, self.user.id))

    def test_is_subscribed_invalid(self):
        self.assertFalse(Subscription.objects.is_subscribed(None, None))
