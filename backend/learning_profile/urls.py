from django.urls import path, include

from . import views
app_name = 'profile'

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('login', views.login, name='login'),
    path('password', views.find_password, name='password'),
    path('resetpwd', views.verify_password, name='resetpwd'),
    path('changepwd', views.change_password, name='changepwd'),
    path('modify_profile', views.modify_basic_information, name='modify_profile'),

]