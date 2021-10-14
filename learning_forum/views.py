from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from learning_profile.models import User
from learning_forum.models import Comments, Posts
import json
import learning_forum.utils as utils


@require_http_methods(["POST"])
def get_posts(request):
    response = {}
    try:
        payload = json.loads(request.body.decode())

        current_user = payload.get("user")
        # TODO Pagination
        # TODO User authentication
        uid = current_user["userId"]
        user = User.objects.get(id=uid)

        # TODO order by created_at
        posts = Posts.objects.all().order_by("-created_at")     # -created_at => created_at DESC
        print(posts)
        response["posts"] = []
        for p in posts:
            response["posts"].append(
                {
                    "avatar": p.user.profile_image,
                    "name": p.user.first_name + " " + p.user.last_name,
                    "date": p.created_at,
                    "content": p.content,
                    # TODO liked
                    "liked": 0,
                    "goal": p.post_type,    # post_type: 1 -> trivial post, 2 -> goal post
                }
            )
        # MOCKED DATA
        # response[posts"] = [
        #     {
        #         "avatar": "https://encrypted-tbn0.gstatic.\
        #         com/images?q=tbn:ANd9GcTF6gxcpCNbqxso3AXdPSq41k-bLC0udTNR3w&usqp=CAU",
        #         "name": "Baocheng Wang", "date": "2021-10-28", "comment": "ELEC3609 get HD", "liked": 1,
        #         "goal": 1},
        #     {"avatar": "", "name": "Alan Kang", "date": "2021-10-27", "comment": "ELEC3609 get PS", "liked": 0,
        #      "goal": 1},
        #     {"avatar": "", "name": "Yanhao Xu", "date": "2021-10-26", "comment": "ELEC3609 get DI", "liked": 0,
        #      "goal": 1},
        #     {"avatar": "", "name": "Alan Kang", "date": "2021-10-25", "comment": "I am Baocheng's Son", "liked": 1,
        #      "goal": 0},
        #     {"avatar": "", "name": "Baocheng Wang", "date": "2021-10-24", "comment": "Hello Food", "liked": 0,
        #      "goal": 0},
        #     {"avatar": "", "name": "Baocheng Wang", "date": "2021-10-23", "comment": "Hello, World", "liked": 1,
        #      "goal": 0},
        # ]
        print(response["posts"])
        response['status'] = "success"
    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to transmit'
        print(e)
        print("ERROR in COMMENT")
    return JsonResponse(response)


@require_http_methods(["POST"])
def get_todo(request):
    response = {}
    try:
        user = json.loads(request.body.decode()).get("user")
        # TODO User authentication

        response['todo'] = [
            {"activity": "SOFT3888 Client Meeting", "due": "2021-10-13", "progress": "Completed"},
            {"activity": "INFO3616 Asm 2 Pre", "due": "2021-10-18", "progress": "Ready to submit"},
            {"activity": "ELEC3506 Lab Report 2", "due": "2021-10-20", "progress": "Not Started"},
            {"activity": "ELEC3506 Quiz 2", "due": "2021-11-04", "progress": "Not Started"},
            {"activity": "ELEC3609 Asm3", "due": "2021-11-05", "progress": "Work In Progress"},
        ]

        response['status'] = "success"
    except Exception as e:

        response['status'] = 'failed'
        response['msg'] = 'Failed to transmit'
        print(e)

    return JsonResponse(response)


@require_http_methods(["POST"])
def get_progress(request):
    response = {}
    try:
        user = json.loads(request.body.decode()).get("user")
        # TODO User authentication


        # TODO How to calculate percentage
        a = 11
        b = 15
        percentage = round(a / b * 100, 2)
        if percentage < 0:
            percentage = 0
        elif percentage > 100:
            percentage = 100

        response['color'] = utils.get_color(percentage)
        response['percentage'] = percentage

        response['info'] = "{}/{} tasks are completed".format(a, b)
        response['status'] = "success"
    except Exception as e:

        response['status'] = 'failed'
        response['msg'] = 'Failed to transmit'
        print(e)

    return JsonResponse(response)


@require_http_methods(["POST"])
def like(request):
    response = {}
    try:
        # TODO logic after user hit 'like' button
        response['status'] = "success"
        pass
    except Exception as e:

        response['status'] = 'failed'
        response['msg'] = 'Failed to like'
        print(e)

    return JsonResponse(response)


@require_http_methods(["POST"])
def comment(request):
    response = {}
    try:
        # TODO logic after user hit 'comment' button
        response['status'] = "success"
        pass
    except Exception as e:

        response['status'] = 'failed'
        response['msg'] = 'Failed to comment'
        print(e)

    return JsonResponse(response)


@require_http_methods(["POST"])
def report(request):
    response = {}
    try:
        # TODO logic after user hit 'report' button
        response['status'] = "success"
        pass
    except Exception as e:

        response['status'] = 'failed'
        response['msg'] = 'Failed to report'
        print(e)

    return JsonResponse(response)
