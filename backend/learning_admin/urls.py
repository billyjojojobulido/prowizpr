from django.urls import include, path, re_path

from . import views

app_name = 'admins'

urlpatterns = [
    path('get_users', views.get_users, name='get_users'),
    path('get_posts', views.get_posts, name='get_posts'),
    path('ban_user', views.ban_user, name='ban_user'),
]
