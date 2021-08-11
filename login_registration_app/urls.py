from django.urls import path
from . import views

urlpatterns = [
    path('', views.index), #GET request to display registration and login form
    path('register', views.register), #POST request to register user
    path('login', views.login), #POST request to login user
    path('success', views.success), #GET request to display a specific object's info
    path('logout', views.logout), #POST request to logout user
]