from django.urls import path

from . import views

app_name = 'application'

urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/register', views.Register.as_view(), name="register"),
    path('accounts/login', views.Login.as_view(), name="login"),
    path('accounts/logout', views.logout_view, name="logout"),
    path('about', views.about, name="about"),

    path('connect', views.Connect.as_view(), name="connect"),
    path('room/<str:name>', views.ChatRoom.as_view(), name="room"),

    path('messages/<str:name>', views.Messages.as_view(), name="messages"),
]
