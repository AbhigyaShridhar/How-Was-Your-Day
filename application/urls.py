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
    path('like-minded-people', views.LikeMinded.as_view(), name="like_minded"),

    path('chat/messages/<int:pk>', views.Messages.as_view(), name="messages"),
    path('rooms/messages/<str:name>', views.RoomMessages.as_view(), name="room_messages"),

    path('get-insights', views.Audio.as_view(), name="audio"),
    path('get-heard/<str:topic>', views.People.as_view(), name="get_heard"),
    path('binary_chat/<int:pk>', views.BinaryChat.as_view(), name="binary_chat"),
]
