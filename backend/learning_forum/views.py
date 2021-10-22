from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from learning_profile.models import User
from learning_forum.models import Comments, Posts, Like
from learning_goal.models import Tasks, Goals
import learning_forum.const as const
import json
import learning_forum.utils as utils
import time


@require_http_methods(["POST"])
def show(request):
    first_catch = time.time()
    response = {
        "posts": [],
        "todo": [],
    }
    try:
        # LOADING PARAM
        payload = json.loads(request.body.decode())

        uid = payload.get("user_id")
        # TODO Pagination
        # TODO User authentication
        user = User.objects.get(id=uid)

        # Retrieving Posts data
        posts = Posts.objects.get_all_posts_desc()
        for p in posts:
            ret_p = {
                    "pid": p.id,
                    "avatar": p.user.profile_image,
                    "name": p.user.first_name + " " + p.user.last_name,
                    "date": utils.time_format(p.created_at),
                    "content": p.content,
                    "is_admin": p.user.is_superuser,
                    "liked": Like.objects.check_post_liked(p.id, uid),
                    "goal": p.post_type,  # post_type: 1 -> trivial post, 2 -> goal post
                }
            response["posts"].append(ret_p)

        response['status'] = "success"
    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to transmit'
        print(e)

    final_catch = time.time()
    print("===========================")
    print("Total Time Consumed: {} s".format(final_catch - first_catch))
    print("===========================")
    return JsonResponse(response)


@require_http_methods(["POST"])
def retrieve_goal(request):
    first_catch = time.time()
    response = {
        "todo": [],
    }
    try:
        # LOADING PARAM
        payload = json.loads(request.body.decode())

        uid = payload.get("user_id")
        pid = payload.get("pid")
        # Retrieving Tasks data
        tasks = Tasks.objects.get_tasks_from_pid(pid)

        completed = 0
        total = len(tasks)

        for t in tasks:
            response['todo'].append(
                {
                    "activity": t.content,
                    "due": utils.date_format(t.deadline),
                    "progress": utils.get_progress_msg(t.status),
                    "created_at": t.created_at,
                }
            )
            if t.status == const.STATUS_COMPLETE:
                completed += 1

        # Retrieve Progress
        percentage = 0
        if total != 0:  # caution of division by zero
            percentage = round(completed / total * 100, 2)
        if percentage < 0:
            percentage = 0
        elif percentage > 100:
            percentage = 100

        response['color'] = utils.get_color(percentage)
        response['percentage'] = percentage

        response['info'] = "{}/{} tasks are completed".format(completed, total)
        # TODO get full name from Post using pid
        f_name, l_name = Goals.objects.get_full_name(pid)
        response['goal_user'] = utils.get_full_name(f_name, l_name)

        response['status'] = "success"
        print(response)
    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to transmit'
        print(e)

    final_catch = time.time()
    print("===========================")
    print("Total Time Consumed: {} s".format(final_catch - first_catch))
    print("===========================")
    return JsonResponse(response)


@require_http_methods(["POST"])
def retrieve_comment(request):
    response = {}
    try:
        # LOADING PARAM
        payload = json.loads(request.body.decode())
        pid = int(payload.get("pid"))   # post id

        comments = Comments.objects.get_comments_by_pid_transmit(pid)
        ret_comment = []
        for c in comments:
            ret_comment.append(
                {
                    "cid": c['id'],
                    "content": c['content'],
                    "commenter": utils.get_full_name(c['first_name'], c['last_name']),
                    "comment_time": utils.time_format(c["created_at"]),
                }
            )
        response["comments"] = ret_comment
        response['status'] = "success"
        pass
    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to comment'
        print(e)

    return JsonResponse(response)


@require_http_methods(["POST"])
def write_comment(request):
    response = {}
    try:
        # LOADING PARAM
        payload = json.loads(request.body.decode())
        uid = payload.get("user_id")
        pid = payload.get("pid")
        content = payload.get("content")

        ack = Comments.objects.write_comment(pid, uid, content)
        if ack:
            response['status'] = "success"
        else:
            response['status'] = "failed"
    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to leave comment'
        print(e)

    return JsonResponse(response)


@require_http_methods(["POST"])
def report_post(request):
    response = {}
    try:
        payload = json.loads(request.body.decode())
        # No need for authentication
        pid = int(payload.get("pid"))   # post id

        Posts.objects.report_post(pid)
        response['status'] = "success"
    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to report'
        print(e)
    return JsonResponse(response)


@require_http_methods(["POST"])
def like_post(request):
    response = {}
    try:
        payload = json.loads(request.body.decode())
        uid = payload.get("user_id")
        pid = payload.get("post_id")    # post id
        like = int(payload.get("like"))     # like or dislike
        # Like
        if like == const.LIKE_LIKE:
            Like.objects.like_post(pid, uid)
        elif like == const.LIKE_DISLIKE:
            Like.objects.dislike_post(pid, uid)
        response['status'] = "success"
        pass
    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to like'
        print(e)

    return JsonResponse(response)
