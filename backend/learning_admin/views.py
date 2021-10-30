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
        users = User.objects.filter(is_superuser=False)
        print(users)
        for u in users:
            user = {
                "uid": u.id,
                "name": utils.get_full_name(u.first_name, u.last_name),
            }
            # Profile Image Null Check
            if u.profile_image is None:
                user["avatar"] = 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
            else:
                user["avatar"] = u.profile_image
            # Status Decode
            if u.is_active:
                user["status"] = "Active"
            else:
                user["status"] = "Banned"
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
                "content": p.content,
            }
            # POST publish status decode
            if p.status == const.POST_PUBLISH_STATUS_PUBLIC:
                post["publish"] = "Public"
            elif p.status == const.POST_PUBLISH_STATUS_PRIVATE:
                post["publish"] = "Private"
            # POST status decode
            if p.active == const.POST_STATUS_ACTIVE:
                post["status"] = "Active"
            elif p.active == const.POST_STATUS_BANNED:
                post["status"] = "Banned"
            response["posts"].append(post)
        response['status'] = 'success'

    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to retrieve posts'
        print(e)
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def ban_user(request):
    response = {}
    try:
        # LOADING PARAM
        payload = json.loads(request.body.decode())
        uid = payload.get("user_id")
        print("Banning User: {}".format(uid))
        # Retrieve User
        user = User.objects.get(pk=uid)
        if user is None:
            # Invalid User Check
            response['status'] = 'failed'
            response['msg'] = 'No such user'
        else:
            # Transform status
            user.is_active = const.USER_ACCOUNT_BANNED
            user.save()
            response['status'] = 'success'
    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to ban user'
        print(e)
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def restore_user(request):
    response = {}
    try:
        # LOADING PARAM
        payload = json.loads(request.body.decode())
        uid = payload.get("user_id")
        # Retrieve User
        user = User.objects.get(pk=uid)
        if user is None:
            # Invalid User Check
            response['status'] = 'failed'
            response['msg'] = 'No such user'
        else:
            # Transform status
            user.is_active = const.USER_ACCOUNT_ACTIVE
            user.save()
            response['status'] = 'success'
    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to restore user'
        print(e)
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def ban_post(request):
    response = {}
    try:
        # LOADING PARAM
        payload = json.loads(request.body.decode())
        pid = payload.get("post_id")
        print("Banning Post: {}".format(pid))
        # Ban the post
        succeed = Posts.objects.ban_a_post_by_pid(pid)
        if succeed:
            response['status'] = 'success'
        else:
            response['status'] = 'failed'
            response['msg'] = 'Failed to ban the post'
    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to ban post'
        print(e)
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def restore_post(request):
    response = {}
    try:
        # LOADING PARAM
        payload = json.loads(request.body.decode())
        pid = payload.get("post_id")

        # Restore the post
        succeed = Posts.objects.restore_a_post_by_pid(pid)
        if succeed:
            response['status'] = 'success'
        else:
            response['status'] = 'failed'
            response['msg'] = 'Failed to restore the post'
    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to restore the post'
        print(e)
    return JsonResponse(response)
