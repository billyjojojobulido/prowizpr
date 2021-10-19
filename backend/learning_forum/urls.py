from django.urls import include, path, re_path

from . import views

app_name = 'forum'

urlpatterns = [
    path('show', views.show, name='show'),
    path('retrieve_goal', views.retrieve_goal, name='retrieve_goal'),
    path('retrieve_comment', views.retrieve_comment, name='retrieve_comment'),
    path('write_comment', views.write_comment, name='write_comment'),
    path('report_post', views.report_post, name='report_post'),
    path('like_post', views.like_post, name='like_post'),
]
