import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.conf.urls import url
from worldChat import consumers as wcconsumers
from ticTacToe import consumers as tttconsumers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FunByte.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r'ws/worldchat/', wcconsumers.ChatConsumer.as_asgi()),
            url(r'ws/ticTacToe/(?P<roomId>[^/]+)/$', tttconsumers.ChatConsumer.as_asgi()),
        ])
    ),
})
