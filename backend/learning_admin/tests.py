from django.test import RequestFactory, TestCase, Client
from .views import *
from learning_profile.models import User
from learning_forum.models import Posts
import json


class AdminViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # Mock Data
        self.user = User.objects.create(
            username="test1234",
            password="1234",
            email="test1234@gmail.com",
            first_name="Unit",
            last_name="Testing",
            is_superuser=False,
            profile_image="something.png",
            is_active=True,
        )
        self.banned_user = User.objects.create(
            username="test5678",
            password="1234",
            email="test5678@gmail.com",
            first_name="Regression",
            last_name="Testing",
            profile_image=None,
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
        self.banned_post = Posts.objects.create(
            user_id=self.user.id,
            content="How you like that",
            status=0,
            active=0,
            likes=0,
            post_type=1,
        )

    def test_get_users(self):
        request = self.factory.get('/admins/get_users')
        response = get_users(request)
        self.assertEqual(response.status_code, 200)

    def test_get_posts(self):
        payload = {
            "user_id": self.user.id,
        }
        request = self.factory.post(
            '/admins/get_posts',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = get_posts(request)
        self.assertEqual(response.status_code, 200)

    def test_ban_user(self):
        payload = {
            "user_id": self.user.id,
        }
        request = self.factory.post(
            '/admins/ban_user',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = ban_user(request)
        target_user = User.objects.get(pk=self.user.id)
        self.assertFalse(target_user.is_active)
        self.assertEqual(response.status_code, 200)

    def test_ban_user_not_exist(self):
        payload = {
            "user_id": 0,
        }
        request = self.factory.post(
            '/admins/ban_user',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = ban_user(request)
        self.assertEqual(response.status_code, 200)

    def test_restore_user(self):
        payload = {
            "user_id": self.banned_user.id,
        }
        request = self.factory.post(
            '/admins/restore_user',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = restore_user(request)
        target_user = User.objects.get(pk=self.banned_user.id)
        self.assertTrue(target_user.is_active)
        self.assertEqual(response.status_code, 200)

    def test_restore_user_not_exist(self):
        payload = {
            "user_id": 0,
        }
        request = self.factory.post(
            '/admins/restore_user',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = restore_user(request)
        self.assertEqual(response.status_code, 200)

    def test_ban_post(self):
        payload = {
            "post_id": self.post.id,
        }
        request = self.factory.post(
            '/admins/ban_post',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = ban_post(request)
        self.assertEqual(response.status_code, 200)
        target_post = Posts.objects.get(pk=self.post.id)
        self.assertFalse(target_post.active)

    def test_ban_post_not_exist(self):
        payload = {
            "post_id": 0,
        }
        request = self.factory.post(
            '/admins/ban_post',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = ban_post(request)
        self.assertEqual(response.status_code, 200)

    def test_restore_post(self):
        payload = {
            "post_id": self.banned_post.id,
        }
        request = self.factory.post(
            '/admins/restore_post',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = restore_post(request)
        self.assertEqual(response.status_code, 200)
        target_post = Posts.objects.get(pk=self.banned_post.id)
        self.assertTrue(target_post.active)

    def test_restore_post_not_exist(self):
        payload = {
            "post_id": 0,
        }
        request = self.factory.post(
            '/admins/restore_post',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = restore_post(request)
        self.assertEqual(response.status_code, 200)
