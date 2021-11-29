#from https://github.com/veryacademy/YT-Django-Project-Chatroom-Getting-Started/blob/master/chat/routing.py

from django.urls import re_path

from . import consumers
from . import consumer_wmtc

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
    re_path('ws/wmtc/', consumer_wmtc.Consumer.as_asgi()), # wmtc = worldmaptestcounter 
]
