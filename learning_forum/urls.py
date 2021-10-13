from django.urls import include, path, re_path

from . import views

app_name = 'forum'

urlpatterns = [
    path('comments', views.get_comments, name='comments'),
    path('todo', views.get_todo, name='todo'),
    path('like', views.like, name='like'),
    path('comment', views.comment, name='comment'),
    path('report', views.report, name='report'),
]
