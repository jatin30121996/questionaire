from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("createAccount/", views.createAccount, name="createAccount"),
    path("login/", views.handlelogin, name="login"),
    path("posted/", views.handlePost, name="handlePost"),
    path("questions/", views.questions, name="questions"),
    path("questions/<str:object>/", views.postanswers, name="postanswers"),
    path("postanswer/", views.answerposted, name="postanswers"),
]