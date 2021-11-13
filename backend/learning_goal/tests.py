from django.test import TestCase, RequestFactory
from learning_profile.models import User
from .views import *
import pytz

class TestGoalModels(TestCase):
    
    def setUp(self):
        self.tz = pytz.timezone("Asia/Shanghai")  # unite time zone
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
    
        self.post = Posts.objects.create(
            user_id=self.user.id,
            content="How you like that",
            status=1,
            active=1,
            likes=10,
            post_type=1,
        )
        
        self.goal = Goals.objects.create(
            likes=10,
            publish_status=1,
            description="Something",
            post_id=self.post.id,
        )
        timestamp = 1462451334
        deadline = datetime.fromtimestamp(timestamp, tz=self.tz)
        self.task = Tasks.objects.create(
            content="Test",
            status=1,
            goal_id=self.goal.id,
            deadline=deadline,
        )

    def test_show(self):
        payload = {
            "user": self.user.id,
        }
        request = self.factory.post(
            '/goal/show',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = show(request)
        content = json.loads(response.content.decode())
        self.assertEqual(len(content['goals']), 1)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_task(self):
        payload = {
            "user_id": self.user.id,
            "gid": self.goal.id,
        }
        request = self.factory.post(
            '/goal/retrieve_task',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = retrieve_task(request)
        content = json.loads(response.content.decode())
        self.assertEqual(len(content['todo']), 1)
        self.assertEqual(response.status_code, 200)

    def test_goal_status(self):
        payload = {
            "status": 0,
            "goalID": self.goal.id,
        }
        request = self.factory.post(
            '/goal/goal_status',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = goal_status(request)
        goal = Goals.objects.get(id=self.goal.id)
        self.assertEqual(goal.publish_status,0)
        self.assertEqual(response.status_code, 200)
    
    def test_task_status(self):
        payload = {
            "status": 2,
            "taskID": self.task.id,
        }
        request = self.factory.post(
            '/goal/task_status',
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = task_status(request)
        task = Tasks.objects.get(id=self.task.id)
        self.assertEqual(task.status, 2)
        self.assertEqual(response.status_code, 200)

    def test_add_goal(self):
        payload = {
            "uid": self.user.id,
            "pid": self.post.id,
            "description": "Test Goals"
        }
        request = self.factory.post(
            '/goal/add_goal',
            data=json.dumps(payload),
            content_type='application/json'
        )
        add_goal(request)
        goals = Goals.objects.filter(post__user_id=self.user.id)
        self.assertEqual(len(goals),2)
    
    def test_add_task(self):
        payload = {
            "gid": self.goal.id,
            "content": "Test task",
            "deadline": str(datetime.now()),
        }
        request = self.factory.post(
            '/goal/add_task',
            data=json.dumps(payload),
            content_type='application/json'
        )
        print('AAAAAAA')
        add_task(request)
        tasks = Tasks.objects.filter(goal_id=self.goal.id)
        print(self.goal.id)
        # self.assertEqual(response.status_code, 200)
        print(tasks)

        print('AAAAAAA')
        self.assertEqual(len(tasks), 2)

    def test_retrieve_goals_desc_length(self):
        goals = Goals.objects.get_all_goals_desc()
        self.assertEqual(len(goals), 1)

    def test_check_likes(self):
        Goals.objects.check_goals_liked(self.goal.id)
        goal = Goals.objects.get(pk=self.goal.id)
        self.assertEqual(goal.likes , 10)

    def test_check_likes_fail(self):
        self.assertFalse(Goals.objects.check_goals_liked(0))

    def test_get_full_name_by_pid(self):
        first_name, last_name = Goals.objects.get_full_name(self.goal.id)
        self.assertEqual(first_name, "Unit")
        self.assertEqual(last_name, "Testing")

    def test_add_goal(self):
        Goals.objects.add_goal(self.post.id, "test")
        goals = Goals.objects.get_all_goals_desc()
        self.assertEqual(len(goals), 2)

    def test_add_goal_fail(self):
        self.assertFalse(Goals.objects.add_goal(0,'test'))

    
    def test_get_task_from_pid(self):
        global post_id
        tasks = Tasks.objects.get_tasks_from_pid(self.post.id)
        self.assertEqual(len(tasks) , 1)


