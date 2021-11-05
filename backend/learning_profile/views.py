import time
import json
import re
from datetime import datetime, timedelta
from random import Random
from threading import Thread

from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth import authenticate, get_user_model, logout
from django.middleware.csrf import get_token
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from goal_project import settings
from .forms import CustomUserCreationForm

User = get_user_model()
DEFAULT_IMAGE_URL = "https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"


@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    response = {}
    verification_code = request.POST["verify_code"]
    username = request.POST["username"]
    saved_code = cache.get("reg_" + username)
    if saved_code != verification_code:
        response["status"] = "failed"
        response["msg"] = "verification code does not match"
    else:
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            response["status"] = "success"
            response["msg"] = "The user has successfully registered"
            cache.delete("reg_" + username)
        else:
            error_info = form.errors.as_json()
            data = json.loads(error_info)
            response["status"] = "failed"
            response["msg"] = tuple(data.items())[0][1]
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def register_email(request):
    response = {}
    try:
        payload = json.loads(request.body.decode())
        username = payload.get("username")
        email = payload.get("email")
        user = User.objects.filter(username=username)
        if len(user) > 0:
            response["status"] = "failed"
            response["msg"] = "this username has been registered"
            return JsonResponse(response)

        code = random_code()
        print("Verification Code is: {}".format(code))
        email_thread = Thread(target=send_mail, args=(
            "WELCOME!",
            "the verification code for signing up the study forum is %s, the code will become invalid in 60 seconds" % code,
            settings.EMAIL_HOST_USER,
            [email, ]
        ))

        email_thread.start()
        key = "reg_" + username
        cache.set(key, code, 60)
        response["code"] = code
        response["status"] = "success"
        response["msg"] = "verification code successfully saved"
        res = JsonResponse(response)
        res.set_cookie("expire_time", datetime.now() + timedelta(seconds=60), max_age=60)
        return res
    except Exception as e:
        print(e)
        response["status"] = "failed"
        response["msg"] = "redis internal error, check the connection"
        return JsonResponse(response)


@csrf_exempt
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
            print(get_token(request))
            response["status"] = "success"
            response["msg"] = "log in"
            response["uid"] = user.id
            response["is_admin"] = user.is_superuser
    except Exception as e:
        response["status"] = "failed"
        response["msg"] = "failed to log in"
        print(e)
    print(response)
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def user_exit(request):
    logout(request)
    response = {"status": "success", "msg": "the user have been logged out"}
    return JsonResponse(response)


def random_code(length=6):
    rand_str = ''
    chars = '0123456789'
    random = Random()
    for i in range(length):
        rand_str += chars[random.randint(0, length)]
    return rand_str


@csrf_exempt
@require_http_methods(["POST"])
def find_password(request):
    response = {}
    payload = json.loads(request.body.decode())
    username = payload.get("username")
    verification_code = random_code()
    print("Verification Code is {}".format(verification_code))
    try:
        user = User.objects.get(username=username)
        last_email_time = user.email_code_time
        current_time = time.time()
        seconds = int(current_time) - last_email_time
        if seconds < 60:
            response["status"] = "failed"
            response["msg"] = "send the email again in {} seconds".format(seconds)
            response["time"] = seconds
            return JsonResponse(response)

        key = "pwd_" + user.username
        cache.set(key, verification_code, 60)
        email_thread = Thread(target=send_mail, args=(
            "reset your password",
            "the verification code for the study forum is %s" % verification_code,
            settings.EMAIL_HOST_USER,
            [user.email, ]
        ))
        email_thread.start()
        user.email_code_time = time.time()
        user.save()
        response["status"] = "success"
        response["msg"] = "the verification code is sent"
        response["code"] = verification_code

    except Exception as e:
        print(e)
        response["status"] = "failed"
        response["msg"] = "no such user"
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def verify_password(request):
    response = {}
    payload = json.loads(request.body.decode())
    username = payload.get("username")
    code = payload.get("code")
    password = payload.get("password")
    try:
        user = User.objects.get(username=username)
        user_code = cache.get("pwd_" + user.username)
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
        print(e)
        response["status"] = "failed"
        response["msg"] = "there is no such username"
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def change_password(request):
    response = {}
    payload = json.loads(request.body.decode())
    user_id = payload.get("user_id")
    old_password = payload.get("oldpwd")
    new_password = payload.get("newpwd")
    try:
        user = User.objects.get(id=user_id)
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
            response["msg"] = "success"

    except Exception as e:
        response["status"] = "failed"
        response["msg"] = "no such user"
    return JsonResponse(response)


def check(address):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, address):
        return True
    else:
        return False


@csrf_exempt
@require_http_methods(["POST"])
def modify_basic_information(request):
    response = {}
    payload = json.loads(request.body.decode())
    department = payload.get("department")
    gender = payload.get("gender")
    if gender == "Male":
        gender = 1
    elif gender == "Female":
        gender = 2
    else:
        gender = 3
    userid = payload.get("user_id")
    email = payload.get("email")
    first_name = payload.get("first_name")
    last_name = payload.get("last_name")
    try:
        user = User.objects.get(id=userid)
        if check(email) is False:
            response["status"] = "failed"
            response["msg"] = "invalid email address"
        else:
            user.department = department
            user.gender = gender
            user.email = email
            user.updated_at = timezone.now()
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            response["status"] = "success"
            response["msg"] = "success"
    except Exception as e:
        print(e)
        response["status"] = "failed"
        response["msg"] = "no such user"
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def view_profile(request):
    response = {}
    payload = json.loads(request.body.decode())
    userid = payload.get("user_id")
    try:
        user = User.objects.get(id=userid)
        info = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username,
            "image": user.profile_image is None ,
            "gender": user.gender,
            "department": user.department
        }
        # If user has not uploaded any profile image, use Default one
        if user.profile_image is None:
            info["image"] = DEFAULT_IMAGE_URL
        else:
            info["image"] = user.profile_image

        response["info"] = info
        response["status"] = "success"
        response["msg"] = "get information successfully"
    except Exception as e:
        response["status"] = "failed"
        response["msg"] = "no such user"
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def upload_image(request):
    response = {}
    payload = json.loads(request.body.decode())
    userid = payload.get("user_id")
    url = payload.get("url")
    try:
        user = User.objects.get(id=userid)
        user.profile_image = url
        user.save()
        response["status"] = "success"
        response["msg"] = "success"
    except Exception as e:
        response["status"] = "failed"
        response["msg"] = "no such user"
    return JsonResponse(response)
