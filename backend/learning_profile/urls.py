from django.urls import path, include

from . import views
app_name = 'profile'

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('login', views.login, name='login'),
    path('password', views.find_password, name='password')
]