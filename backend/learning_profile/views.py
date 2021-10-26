import time
import json
from random import Random
from threading import Thread
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate
from django.views.decorators.http import require_http_methods
from goal_project import settings
from .forms import CustomUserCreationForm

User = get_user_model()


@require_http_methods(["POST"])
def register(request):
    response = {}
    form = CustomUserCreationForm(data=request.POST)
    print(request.POST)
    if form.is_valid():
        new_user = form.save()
        response["status"] = "success"
        response["msg"] = "The user has successfully registered"
    else:
        error_info = form.errors.as_json()
        data = json.loads(error_info)
        response["status"] = "failed"
        response["msg"] = tuple(data.items())[0][1]
        print(data)
    return JsonResponse(response)


@require_http_methods(["POST"])
def login(request):
    response = {}
    try:
        payload = json.loads(request.body.decode())
        username = payload.get("username")
        password = payload.get("password")
        print("Username: {}".format(username))
        print("Password: {}".format(password))
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
            last_email_time = user.email_code_time
            current_time = time.time()
            seconds = int(current_time) - last_email_time
            if seconds < 60:
                response["status"] = "failed"
                response["msg"] = "send the email again in {} seconds".format(seconds)
                response["time"] = seconds
                return JsonResponse(response)

            email_thread = Thread(target=send_mail, args=(
                "reset your password",
                "the verification code for the study forum is %s" % verification_code,
                settings.EMAIL_HOST_USER,
                [user.email, ]
            ))
            email_thread.start()
            user.email_code = verification_code
            user.email_code_time = time.time()
            user.save()
            response["status"] = "success"
            response["msg"] = "the verification code is sent"
            # TODO will delete
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


@require_http_methods(["POST"])
def verify_password(request):
    response = {}
    payload = json.loads(request.body.decode())
    username = payload.get("username")
    code = payload.get("code")
    password = payload.get("password")
    user = User.objects.get(username=username)
    if user is not None:
        user_code = user.email_code
        try:
            if code != user_code:
                response["status"] = "failed"
                response["msg"] = "verification code does not match"
            elif user.check_password(password) is True:
                response["status"] = "failed"
                response["msg"] = "the password is same as the previous one"
            else:
                user.set_password(password)
                user.save()
                response["status"] = "success"
                response["msg"] = "successfully changed the password"
        except Exception as e:
            response["status"] = "failed"
            response["msg"] = "internal error: {}".format(e)
    else:
        response["status"] = "failed"
        response["msg"] = "there is no such username"
    return JsonResponse(response)


@require_http_methods(["POST"])
def change_password(request):
    response = {}
    payload = json.loads(request.body.decode())
    username = payload.get("username")
    old_password = payload.get("oldpwd")
    new_password = payload.get("newpwd")
    user = User.objects.get(username=username)
    if user is not None:
        validation = user.check_password(old_password)
        new_validation = user.check_password(new_password)
        if validation is False:
            response["status"] = "failed"
            response["msg"] = "the password does not match"
        elif new_validation is True:
            response["status"] = "failed"
            response["msg"] = "the password is same as the previous one"
        else:
            user.set_password(new_password)
            user.save()
            response["status"] = "success"
            response["msg"] = "the password has been reset"
    else:
        response["status"] = "failed"
        response["msg"] = "no such user"
    return JsonResponse(response)


