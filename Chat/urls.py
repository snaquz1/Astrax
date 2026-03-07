from django.urls import path

from Chat.views import *

urlpatterns = [
    path("ws-demo/", ws_demo, name="ws-demo"),
    path('', index, name='index'),
path("createchat", create_chat, name='create_chat'),
    path("ws/chat/<int:chat_id>", chat_room, name="chat_room"),

]