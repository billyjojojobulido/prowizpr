from django.urls import include, path, re_path

from . import views

app_name = 'forum'

urlpatterns = [
    path('show', views.show, name='show'),
    path('like', views.like, name='like'),
    path('comment', views.comment, name='comment'),
    path('report', views.report, name='report'),
]
