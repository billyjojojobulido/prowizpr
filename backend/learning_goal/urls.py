from django.urls import include, path, re_path

from . import views

app_name = 'goal'

urlpatterns = [
    path('show', views.show, name='show'),
    path('retrieve_goal', views.retrieve_goal, name='retrieve_goal'),

]