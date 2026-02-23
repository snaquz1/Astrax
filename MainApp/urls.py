from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path("send/<int:chat_id>/", send, name='send'),
    path("poll/<int:chat_id>/", poll, name='poll'),
    path("createchat", create_chat, name='create_chat')
]