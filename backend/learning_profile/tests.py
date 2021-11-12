from django.test import TestCase, RequestFactory
from unittest import TestCase as UnitTestCase
from .views import *

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
            gender=1,
            first_name="Unit",
            last_name="Testing",
            department="FEIT",
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

    def test_login(self):
        payload = {
            "username": self.user.username,
            "password": self.user.password,
        }
        request = self.factory.post(
            '/profile/login',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = login(request)
        self.assertEqual(response.status_code, 200)

    def test_upload_image(self):
        payload = {
            "username": self.user.username,
            "url":"https://b-ssl.duitang.com/uploads/item/201711/28/20171128135548_AdaGx.thumb.700_0.jpeg",
        }
        request = self.factory.post(
            '/profile/login',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = upload_image(request)
        self.assertEqual(response.status_code, 200)

    def test_view_profile(self):
        payload = {
            "user_id": self.user.id,
        }
        request = self.factory.post(
            '/profile/information',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = view_profile(request)
        self.assertEqual(response.status_code, 200)
    
    def test_modify_basic_information(self):
        payload = {
            "user_id": self.user.id,
            "department": self.user.department,
            "email": self.user.email,
            "gender": self.user.gender,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
        }
        request = self.factory.post(
            '/profile/modify_profile',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = modify_basic_information(request)
        self.assertEqual(response.status_code, 200)

    def test_change_password(self):
        payload = {
            "user_id": self.user.id,
            "old_password": self.user.password,
            "new_password": "12345"
        }
        request = self.factory.post(
            '/profile/modify_profile',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = change_password(request)
        self.assertEqual(response.status_code, 200)
