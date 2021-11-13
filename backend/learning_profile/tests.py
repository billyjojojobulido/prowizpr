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
        )

    def test_user_name(self):
        self.assertEqual(User.objects.get(pk=self.user.id).username,"test1234")

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
            "username": "test1234",
            "password": "1234",
        }
        request = self.factory.post(
            '/profile/login',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = login(request)
        content = json.loads(response.content.decode())  
        self.assertEqual(content['status'],'success')
        self.assertEqual(response.status_code, 200)

    def test_change_password(self):
        payload = {
            "user_id": self.user.id,
            "oldpwd": "1234",
            "newpwd": "12345",
        }
        request = self.factory.post(
            '/profile/changepwd',
            data=json.dumps(payload),
            content_type='application/json'
        )
        change_password(request)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.password,'12345')

    def test_verify_password(self):
        payload = {
            "username": self.user.username,
            "old_password": self.user.password,
            "code": "12345"
        }
        request = self.factory.post(
            '/profile/resetpwd',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = verify_password(request)
        self.assertEqual(response.status_code, 200)
    
    def test_modify_basic_information(self):
        payload = {
            "user_id": self.user.id,
            "department": 'SIT',
            "email": 'test1234@outlook.com',
            "gender": 2,
            "first_name": 'test',
            "last_name": 'T',
        }
        request = self.factory.post(
            '/profile/modify_profile',
            data=json.dumps(payload),
            content_type='application/json'
        )
        modify_basic_information(request)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.department, 'SIT')
        self.assertEqual(user.email, 'test1234@outlook.com')
        self.assertEqual(user.gender, 2)
        self.assertEqual(user.first_name, 'test')
        self.assertEqual(user.last_name, 'T')


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
        content = json.loads(response.content.decode()) 
        self.assertEqual(len(content['info']),7)
        self.assertEqual(response.status_code, 200)

    def test_upload_image(self):
        payload = {
            "user_id": self.user.id,
            "url":"https://b-ssl.duitang.com/uploads/item/201711/28/20171128135548_AdaGx.thumb.700_0.jpeg",
        }
        request = self.factory.post(
            '/profile/upload_image',
            data=json.dumps(payload),
            content_type='application/json'
        )
        upload_image(request)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.profile_image, "https://b-ssl.duitang.com/uploads/item/201711/28/20171128135548_AdaGx.thumb.700_0.jpeg")
        # self.assertEqual(response.status_code, 200)