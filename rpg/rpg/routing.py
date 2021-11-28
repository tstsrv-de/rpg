# from https://github.com/veryacademy/YT-Django-Project-Chatroom-Getting-Started/blob/master/core/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import rjh_rpg.routing


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            rjh_rpg.routing.websocket_urlpatterns
        )
    ),
})