from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json


@require_http_methods(["POST"])
def show(request):
    response = {}
    try:
        user = json.loads(request.body.decode()).get("user")
        # TODO User authentication
        print(user)

        # TODO DB query
        comments = [
            {"avatar": "", "name": "Baocheng Wang", "date": "2021-10-28", "comment": "ELEC3609 get HD", "liked": 1,
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

        response = {'status': 'success', 'comments': comments}
        # allows the query to proceed
    except Exception as e:
        response['status'] = 'success'
        response['query'] = ''
        print(e)
    print(response)
    return JsonResponse(response)
