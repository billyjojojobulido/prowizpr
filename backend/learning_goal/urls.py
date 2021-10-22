from django.urls import include, path, re_path

from . import views

app_name = 'goal'

urlpatterns = [
    path('show', views.show, name='show'),
    path('retrieve_task', views.retrieve_task, name='retrieve_task'),
    path('add_goal', views.Add_Goal, name='add_goal'),
    path('add_task', views.Add_Task, name='add_task'),

]