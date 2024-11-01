from django.urls import include, path, re_path

from . import views

app_name = 'admins'

urlpatterns = [
    path('get_users', views.get_users, name='get_users'),
    path('get_posts', views.get_posts, name='get_posts'),
    path('ban_user', views.ban_user, name='ban_user'),
    path('restore_user', views.restore_user, name='restore_user'),
    path('ban_post', views.ban_post, name='ban_post'),
    path('restore_post', views.restore_post, name='restore_post'),
]
