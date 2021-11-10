from django.test import TestCase
from unittest import TestCase as UnitTestCase
from datetime import datetime
import learning_forum.utils as utils
from learning_profile.models import User
from learning_forum.models import Posts
from learning_goal.models import Goals,Tasks
import pytz


class TestGoalUtils(UnitTestCase):

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

    
user_id = 0
post_id = 0
goal_id = 0
task_id = 0



class TestGoalModels(TestCase):

    def setUp(self):
        user = User.objects.create(
            username="test1234",
            password="1234",
            email="test1234@gmail.com",
            first_name="Unit",
            last_name="Testing",
            is_superuser=False,
            is_active=True,
        )
    
        post = Posts.objects.create(
            user_id=user.id,
            content="How you like that",
            status=1,
            active=1,
            likes=10,
            post_type=1,
        )
        
        goal = Goals.objects.create(
            likes=10,
            publish_status=1,
            description="Something",
            post_id=post.id,
        )

        task = Tasks.objects.create(
            content = "Test",
            status = 1,
            goal_id = goal.id,
        )
        global user_id, post_id, goal_id,task_id
        user_id = user.id
        post_id = post.id
        goal_id = goal.id
        task_id = task.id

    def test_set_up(self):
        global post_id, goal_id
        self.assertNotEqual(post_id, 0)
        self.assertNotEqual(goal_id, 0)

    def test_retrieve_goals_desc_length(self):
        goals = Goals.objects.get_all_goals_desc()
        self.assertEqual(len(goals), 1)

    def test_check_likes(self):
        global goal_id
        Goals.objects.check_goals_liked(goal_id)
        goal = Goals.objects.get(pk=goal_id)
        self.assertEqual(goal.likes , 10)
    def test_check_likes_fail(self):
        global goal_id
        self.assertFalse( Goals.objects.check_goals_liked(0))


    def test_get_full_name_by_pid(self):
        global goal_id
        first_name, last_name = Goals.objects.get_full_name(goal_id)
        self.assertEqual(first_name, "Unit")
        self.assertEqual(last_name, "Testing")

    def test_add_goal(self):
        global post_id
        Goals.objects.add_goal(post_id,"test")
        goals = Goals.objects.get_all_goals_desc()
        self.assertEqual(len(goals) , 2)

    def test_add_goal_fail(self):
        self.assertFalse(Goals.objects.add_goal(0,'test'))

    
    def test_get_task_from_pid(self):
        global post_id
        tasks = Tasks.objects.get_tasks_from_pid(post_id)
        self.assertEqual(len(tasks) , 1)


