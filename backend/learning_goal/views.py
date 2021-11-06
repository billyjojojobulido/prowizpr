from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from learning_forum.models import Posts
from learning_goal.models import Tasks, Goals
import learning_forum.const as const
import json
import learning_goal.utils as utils
import time
from datetime import datetime


@csrf_exempt
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
        uid = payload.get("user")
        # Retrieving Goals data for specific user
        goals = Goals.objects.filter(post__user_id=uid)
        print(uid)
        print(goals)
        for g in goals:
            ret_g = {
                "gid": g.id,
                "date": utils.time_format(g.created_at),
                "description": g.description,
                "liked": g.likes,
                "publish": utils.get_publish_msg(g.publish_status)  # publish_status: 1 -> public, 2 -> private
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


@csrf_exempt
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
        gid = payload.get("gid")
        # Retrieving Tasks data
        tasks = Tasks.objects.filter(goal_id=gid)
        completed = 0
        total = len(tasks)

        for t in tasks:
            response['todo'].append(
                {
                    "tid":t.id,
                    "activity": t.content,
                    "due": utils.date_format(t.deadline),
                    "progress": utils.get_progress_msg(t.status),# 1->To Do, 2->In Progress, 3->Done
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
        f_name, l_name = Goals.objects.get_full_name(gid)
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


@csrf_exempt
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
        #create data into database
        ack1 = Posts.objects.create(likes=0,
                                    status=1,
                                    content=description,
                                    post_type=2,
                                    user_id=uid,
                                    report_times=0)
        print(ack1)
        ack = Goals.objects.create(likes=0,
                                   publish_status=1,
                                   description=description,
                                   post_id=ack1.id)
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


@csrf_exempt
@require_http_methods(["POST"])
def add_task(request):
    first_catch = time.time()
    response = {}
    try:
        # LOADING PARAM
        payload = json.loads(request.body.decode())
        goal_id = payload.get("gid")
        content = payload.get("content")
        deadline = datetime.strptime(payload.get("deadline"), '%Y-%m-%d %H:%M:%S.%f')
        #create data into tasks table
        ack = Tasks.objects.create(content=content,
                                   deadline=utils.date_format(deadline),
                                   status=1,
                                   goal_id=goal_id)
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


@csrf_exempt
@require_http_methods(["POST"])
def goal_status(request):
    response = {}
    try:
        payload = json.loads(request.body.decode())
        status = payload.get("status")
        goal_id = payload.get("goalID")
        goal = Goals.objects.get(id=goal_id)
        post = Posts.objects.get(id=goal.post_id)
        goal.publish_status = status
        post.status = status
        goal.save()
        post.save()
        response['status'] = 'success'
        response['msg'] = 'successfully update the status of the goal'
    except Exception as e:
        print(e)
        response['status'] = 'failed'
        response['msg'] = 'failed to change the status of goal'

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def task_status(request):
    response = {}
    try:
        payload = json.loads(request.body.decode())
        status = payload.get("status")
        task_id = payload.get("taskID")
        task = Tasks.objects.get(id=task_id)
        task.status = status
        task.save()

        response['status'] = 'success'
        response['msg'] = 'successfully update the status of the task'
    except Exception as e:
        print(e)
        response['status'] = 'failed'
        response['msg'] = 'failed to change the status of task'
    return JsonResponse(response)
