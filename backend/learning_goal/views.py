from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from learning_profile.models import User
from learning_forum.models import Comments, Posts, Like
from learning_goal.models import Tasks, Goals
import learning_goal.const as const
import json
import learning_goal.utils as utils
import time


@require_http_methods(["POST"])
def show(request):
    first_catch = time.time()
    response = {
        "goals": [],
        "todo": [],
    }
    try:
        # LOADING PARAM
        payload = json.loads(request.body.decode())
        # uid = payload.get("user_id")
        # user = User.objects.get(id=uid)

        # pid = payload.get("post_id")
        # print(pid)
        # TODO Pagination
        # TODO User authentication
        # post = Posts.objects.get(id=pid)
        # print("aaaaaaa")

        # Retrieving Posts data
        goals = Goals.objects.get_all_goals_desc()
        for g in goals:
            ret_g = {
                    "gid": g.id,
                    # "avatar": g.user.profile_image,
                    # "name": g.user.first_name + " " + g.user.last_name,
                    "date": utils.time_format(g.created_at),
                    "description": g.description,
                    # "is_admin": g.user.is_superuser,
                    "liked": g.likes,
                    "publish":utils.get_publish_msg(g.publish_status)
                    # "goal": p.post_type,  # post_type: 1 -> trivial post, 2 -> goal post
                }
            response["goals"].append(ret_g)

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
def retrieve_task(request):
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
def add_goal(request):
    first_catch = time.time()
    response = {}
    try:
        # LOADING PARAM
        payload = json.loads(request.body.decode())
        uid = payload.get("uid")
        post_id = payload.get("pid")
        description = payload.get("description")

        print(post_id)
        print(description)
        ack1 = Posts.objects.create(likes=0,
                                    status=1,
                                    content = description,
                                    post_type=2,
                                    user_id = uid,
                                    report_times=0)
        ack = Goals.objects.create(likes=0,
                                   publish_status=1,
                                   description=description,
                                   post_id=post_id)
        if ack and ack1:
            response['status'] = "success"
        else:
            response['status'] = "failed"
    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to leave comment'
        print(e)

    final_catch = time.time()
    print("===========================")
    print("Total Time Consumed: {} s".format(final_catch - first_catch))
    print("===========================")
    return JsonResponse(response)

@require_http_methods(["POST"])
def add_task(request):
    first_catch = time.time()
    response = {}
    try:
        # LOADING PARAM
        payload = json.loads(request.body.decode())
        goal_id = payload.get("gid")
        content = payload.get("content")
        deadline = payload.get("deadline")

        print(goal_id)
        ack = Tasks.objects.create(content = content,
                                   deadline = deadline,
                                   status = 1,
                                   goal_id = goal_id)
        if ack:
            response['status'] = "success"
        else:
            response['status'] = "failed"
    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to leave comment'
        print(e)

    final_catch = time.time()
    print("===========================")
    print("Total Time Consumed: {} s".format(final_catch - first_catch))
    print("===========================")
    return JsonResponse(response)