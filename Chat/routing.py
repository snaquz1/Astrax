from django.urls import re_path, path

from .consumers import *

websocket_urlpatterns = [
    path("ws/ping/", PingConsumer.as_asgi()),
    path("ws/chat/<int:chat_id>/", ChatConsumer.as_asgi())
]
