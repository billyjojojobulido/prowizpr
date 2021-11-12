from django.test import TestCase, RequestFactory
from unittest import TestCase as UnitTestCase
from datetime import datetime

from django.test.utils import register_lookup
from backend.learning_profile.views import register_email

from learning_profile.models import User

import pytz

user_id = 0

class TestProfileModels(TestCase):

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
        global user_id
        user_id = self.user.id
    
    def test_set_up(self):
        global user_id
        self.assertNotEqual(user_id, 0)

    def test_user_name(self):
        global user_id
        self.assertEqual(User.objects.get(pk=user_id).username,"test1234")

    def test_register_email(self):
        payload = {
            "username": self.user.username,
            "email": self.user.email,
        }
        request = self.factory.post(
            '/profile/reg_email',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = register_email(request)
        self.assertEqual(response.status_code, 200)
