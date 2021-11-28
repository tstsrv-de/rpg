#from https://github.com/veryacademy/YT-Django-Project-Chatroom-Getting-Started/blob/master/chat/routing.py

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
]
