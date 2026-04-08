from django.urls import path

from Chat.views import *

urlpatterns = [
    path('', index, name='index'),
    path("createchat", create_chat, name='create_chat'),
    path("chat/<int:chat_id>/send", send_message, name='send_message'),
    path("invite/<str:token>", invite, name='invite'),
    path("deletechat/<int:chat_id>", delete_chat, name='delete_chat'),
    path("error", error, name='error'),
    path("manage/<int:chat_id>/<int:member_id>/<str:operation>", manage_user, name='manage_user'),
]