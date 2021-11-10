from django.test import TestCase
from unittest import TestCase as UnitTestCase
from datetime import datetime

from learning_profile.models import User
from learning_profile.forms import CustomUserCreationForm

import pytz

user_id = 0

class TestProfileModels(TestCase):

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
        global user_id
        user_id = user.id
    
    def test_set_up(self):
        global user_id
        self.assertNotEqual(user_id, 0)

    def test_user_name(self):
        global user_id
        self.assertEqual(User.objects.get(pk=user_id).username,"test1234")

class TestForm(TestCase):
    def setUp(self):
        