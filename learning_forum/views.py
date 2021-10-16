from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from learning_profile.models import User
from learning_forum.models import Comments, Posts
from learning_goal.models import Tasks
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

        current_user = payload.get("user")
        # TODO Pagination
        # TODO User authentication
        uid = current_user["userId"]
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
                    # TODO liked
                    "liked": 0,
                    "goal": p.post_type,  # post_type: 1 -> trivial post, 2 -> goal post
                }
            response["posts"].append(ret_p)

        # Retrieving Tasks data
        tasks = []
        if posts is not None and len(posts) > 0:
            tasks = Tasks.objects.get_tasks_from_gid(posts[0].id)

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
        # TODO logic after user hit 'write comment' button
        response['status'] = "success"
        pass
    except Exception as e:

        response['status'] = 'failed'
        response['msg'] = 'Failed to report'
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
