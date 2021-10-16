from django.urls import include, path, re_path

from . import views

app_name = 'forum'

urlpatterns = [
    path('show', views.show, name='show'),
    path('like', views.like, name='like'),
    path('retrieve_comment', views.retrieve_comment, name='retrieve_comment'),
    path('write_comment', views.write_comment, name='write_comment'),
    path('report', views.report, name='report'),
]
