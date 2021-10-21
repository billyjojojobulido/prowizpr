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
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        response["status"] = "success"
        response["msg"] = "The user has successfully logged in"
    else:
        response["status"] = "failed"
        response["msg"] = "the user does not exist or the password does not match"
    return JsonResponse(response)
