from django.urls import include, path, re_path

from . import views

app_name = 'forum'

urlpatterns = [
    path('show', views.show, name='show'),
]