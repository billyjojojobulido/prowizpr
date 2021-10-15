# from django.test import TestCase
from unittest import TestCase
from datetime import datetime
import learning_forum.utils as utils
import pytz


class TestForum(TestCase):

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


        