from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from learning_profile.models import User
from learning_forum.models import Comments, Posts, Like
from learning_goal.models import Tasks, Goals
import learning_forum.const as const
import json
import learning_forum.utils as utils
import time


@require_http_methods(["GET"])
def get_users(request):
    first_catch = time.time()   # Timing
    response = {
        "users": [],
    }
    try:
        # Retrieving Posts data
        users = User.objects.admin_manage_users()
        print(users)
        for u in users:
            user = {
                "avatar": u.profile_image,
                "uid": u.id,
                "name": utils.get_full_name(u.first_name, u.last_name),
                "is_active": u.is_active,
            }
            response["users"].append(user)

        response['status'] = "success"
    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to retrieve users'
        print(e)

    final_catch = time.time()
    print("===========================")
    print("Total Time Consumed: {} s".format(final_catch - first_catch))    # timing
    print("===========================")
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def get_posts(request):
    response = {
        "posts": [],
    }
    try:
        # LOADING PARAM
        payload = json.loads(request.body.decode())
        uid = payload.get("user_id")
        # Retrieve all posts owned by a user
        posts = Posts.objects.get_posts_by_uid(uid)
        # extracting data
        for p in posts:
            post = {
                "pid": p.id,
                "created_at": utils.time_format(p.created_at),
                "likes": p.likes,
                "reports": p.report_times,
                "status": p.status,
            }
            response["posts"].append(post)

        response['status'] = 'success'

    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to retrieve posts'
        print(e)
    return JsonResponse(response)

