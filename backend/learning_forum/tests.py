from django.test import TestCase
from unittest import TestCase as UnitTestCase
from datetime import datetime
import learning_forum.utils as utils
from learning_profile.models import  User
from learning_forum.models import Posts, Comments, Like, Subscription
import pytz


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


user_id = 0
post_id = 0
comment_id = 0


class TestForumModels(TestCase):

    def setUp(self):
        user = User.objects.create(
            username="test1234",
            password="1234",
            email="test1234@gmail.com",
            is_superuser=False,
            is_active=True,
        )
        post = Posts.objects.create(
            user_id=user.id,
            content="How you like that",
            status=1,
            active=1,
            likes=0,
            post_type=1,
        )
        Posts.objects.create(
            user_id=user.id,
            content="We dont talk anymore",
            status=2,
            active=1,
            likes=10,
            post_type=1,
        )
        global user_id, post_id, comment_id
        user_id = user.id
        post_id = post.id

    def test_set_up(self):
        global user_id, post_id
        self.assertNotEqual(user_id, 0)
        self.assertNotEqual(post_id, 0)

    def test_retrieve_posts_desc_length(self):
        posts = Posts.objects.get_all_posts_desc()
        self.assertEqual(len(posts), 2)

    def test_retrieve_posts_public_desc_length(self):
        posts = Posts.objects.get_all_posts_desc_public()
        self.assertEqual(len(posts), 1)

    def test_get_post_by_uid(self):
        global user_id
        posts = Posts.objects.get_posts_by_uid(user_id)
        self.assertEqual(len(posts), 2)

    def test_get_post_by_uid_false(self):
        posts = Posts.objects.get_posts_by_uid(0)
        self.assertEqual(len(posts), 0)

    def test_ban_post(self):
        global post_id
        Posts.objects.ban_a_post_by_pid(post_id)
        post = Posts.objects.get(pk=post_id)
        self.assertFalse(post.active)

    def test_ban_not_exist(self):
        self.assertFalse(Posts.objects.ban_a_post_by_pid(0))

    def test_ban_invalid_param(self):
        self.assertFalse(Posts.objects.ban_a_post_by_pid("0"))

    def test_unban_post(self):
        global post_id
        Posts.objects.ban_a_post_by_pid(post_id)
        Posts.objects.restore_a_post_by_pid(post_id)
        post = Posts.objects.get(pk=post_id)
        self.assertTrue(post.active)

    def test_unban_post_not_exist(self):
        self.assertFalse(Posts.objects.restore_a_post_by_pid(0))

    def test_unban_post_invalid_param(self):
        self.assertFalse(Posts.objects.restore_a_post_by_pid("0"))

    def test_report_post(self):
        global post_id
        Posts.objects.report_post(post_id)
        post = Posts.objects.get(pk=post_id)
        self.assertEqual(post.report_times, 1)

    def test_report_clear_after_ban(self):
        global post_id
        Posts.objects.report_post(post_id)
        Posts.objects.ban_a_post_by_pid(post_id)
        post = Posts.objects.get(pk=post_id)
        self.assertEqual(post.report_times, 0)

    def test_like_post(self):
        global post_id
        Posts.objects.like_post(post_id)
        post = Posts.objects.get(pk=post_id)
        self.assertEqual(post.likes, 1)

    def test_dislike_post(self):
        global post_id
        Posts.objects.like_post(post_id)
        Posts.objects.dislike_post(post_id)
        post = Posts.objects.get(pk=post_id)
        self.assertEqual(post.likes, 0)
