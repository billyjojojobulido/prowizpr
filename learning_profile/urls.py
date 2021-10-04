from django.urls import path, include
from django.contrib.auth.views import LoginView

from . import views

app_name = 'profile'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]