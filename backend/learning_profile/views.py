from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
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