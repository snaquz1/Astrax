from django.urls import path

from Chat.views import *

urlpatterns = [
    path("ws-demo/", ws_demo, name="ws-demo"),
    path('', index, name='index'),
    path("createchat", create_chat, name='create_chat'),
    path("invite/<str:token>", invite, name='invite'),
    path("deletechat/<int:chat_id>", delete_chat, name='delete_chat')
]