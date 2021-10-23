from django.http import JsonResponse
from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.http import require_http_methods
import json

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
    return JsonResponse(response)
