from random import Random
from threading import Thread

from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.http import require_http_methods
import json

from goal_project import settings
from .forms import CustomUserCreationForm

User = get_user_model()


# Create your views here.


@require_http_methods(["POST"])
def register(request):
    response = {}
    form = CustomUserCreationForm(data=request.POST)
    if form.is_valid():
        new_user = form.save()
        response["status"] = "success"
        response["msg"] = "The user has successfully registered"
    else:
        error_info = form.errors.as_json()
        data = json.loads(error_info)
        response["status"] = "failed"
        response["msg"] = tuple(data.items())[0][1]
    return JsonResponse(response)


@require_http_methods(["POST"])
def login(request):
    response = {}
    try:
        payload = json.loads(request.body.decode())
        username = payload.get("username")
        password = payload.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            response["status"] = "failed"
            response["msg"] = "user doesn't exists"
        else:
            response["status"] = "success"
            response["msg"] = "log in"
            response["uid"] = user.id
    except Exception as e:
        response["status"] = "failed"
        response["msg"] = "failed to log in"
        print(e)
    print(response)
    return JsonResponse(response)


@require_http_methods(["POST"])
def logout(request):
    response = {}
    logout(request)
    response["status"] = "success"
    response["msg"] = "the user have been logged out"
    return JsonResponse(response)


def random_code(length=6):
    rand_str = ''
    chars = '0123456789'
    random = Random()
    for i in range(length):
        rand_str += chars[random.randint(0, length)]
    return rand_str


@require_http_methods(["POST"])
def find_password(request):
    response = {}
    payload = json.loads(request.body.decode())
    username = payload.get("username")
    user = User.objects.get(username=username)
    verification_code = random_code()
    if user is not None:
        try:
            email_thread = Thread(target=send_mail, args=(
                "reset your password",
                "the verification code for the study forum is %s" % verification_code,
                settings.EMAIL_HOST_USER,
                [user.email, ]
            ))
            email_thread.start()
            response["status"] = "success"
            response["msg"] = "the verification code is sent"
            response["code"] = verification_code
        except Exception as e:
            print(e)
            response["status"] = "failed"
            response["msg"] = e
    else:
        response["msg"] = "failed"
        response["status"] = "there is no such user"
        response["code"] = verification_code
    return JsonResponse(response)
