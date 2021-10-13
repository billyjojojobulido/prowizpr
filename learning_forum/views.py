from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json


@require_http_methods(["POST"])
def get_comments(request):
    response = {}
    try:
        user = json.loads(request.body.decode()).get("user")
        # TODO User authentication
        print(user)

        # TODO DB query
        response["comments"] = [
            {"avatar": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTF6gxcpCNbqxso3AXdPSq41k-bLC0udTNR3w&usqp=CAU", "name": "Baocheng Wang", "date": "2021-10-28", "comment": "ELEC3609 get HD", "liked": 1,
             "goal": 1},
            {"avatar": "", "name": "Alan Kang", "date": "2021-10-27", "comment": "ELEC3609 get PS", "liked": 0,
             "goal": 1},
            {"avatar": "", "name": "Yanhao Xu", "date": "2021-10-26", "comment": "ELEC3609 get DI", "liked": 0,
             "goal": 1},
            {"avatar": "", "name": "Alan Kang", "date": "2021-10-25", "comment": "I am Baocheng's Son", "liked": 1,
             "goal": 0},
            {"avatar": "", "name": "Baocheng Wang", "date": "2021-10-24", "comment": "Hello Food", "liked": 0,
             "goal": 0},
            {"avatar": "", "name": "Baocheng Wang", "date": "2021-10-23", "comment": "Hello, World", "liked": 1,
             "goal": 0},
        ]
        response['status'] = "success"
        # allows the query to proceed
    except Exception as e:
        response['status'] = 'failed'
        response['msg'] = 'Failed to transmit'
        print(e)
    return JsonResponse(response)


@require_http_methods(["POST"])
def get_todo(request):
    response = {}
    try:
        user = json.loads(request.body.decode()).get("user")
        # TODO User authentication
        print(user)

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
        print(user)

        # TODO How to calculate percentage
        a = 11
        b = 15
        percentage = round(a/b * 100, 2)
        if percentage < 0:
            percentage = 0
        elif percentage > 100:
            percentage = 100

        if percentage < 20:
            response['color'] = "#f56c6c"
        elif percentage < 40:
            response['color'] = "#e6a23c"
        elif percentage < 60:
            response['color'] = "#5cb87a"
        elif percentage < 60:
            response['color'] = "#1989fa"
        elif percentage <= 100:
            response['color'] = "#6f7ad3"
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