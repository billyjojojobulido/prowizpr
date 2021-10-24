from django.urls import include, path, re_path

from . import views

app_name = 'goal'

urlpatterns = [
    path('show', views.show, name='show'),
    path('retrieve_task', views.retrieve_task, name='retrieve_task'),
    path('add_goal', views.add_goal, name='add_goal'),
    path('add_task', views.add_task, name='add_task'),
    path('goal_status', views.goal_status, name='goal_status'),
    path("task_status", views.task_status, name='task_status'),
]