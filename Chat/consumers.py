import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.context_processors import request
from Chat.models import *
from channels.db import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def create_message(self, chat_id, text):
        chat = Chat.objects.get(id=chat_id)
        user = self.scope["user"]
        message = Message.objects.create(chat=chat, text=text, username=user)
        return {
            "id": message.id,
            "chat_id": chat_id,
            "text": text,
            "easy": False,
        }

    @sync_to_async
    def in_chat(self, chat_id, user):
        return ChatMember.objects.filter(chat=chat_id, user=user).exists()



    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f"chat_{self.chat_id}"
        self.user = self.scope["user"]
        self.user_group_name = f"user_{self.user.id}"

        if not await self.in_chat(self.chat_id, self.user):
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)

        await self.accept()


    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        data = json.loads(text_data)
        message = data.get("message", "")

        if not message:
            return

        await self.create_message(self.chat_id, message)
        await self.channel_layer.group_send(self.room_group_name, {"type": "chat.message", "message": message, "username": self.scope["user"].username})


    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message, "username": event["username"], "attachments": event.get("attachments", []), "html": event.get("html", "")}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

    async def force_disconnect(self, event):
        if str(self.chat_id) == str(event["chat_id"]):
            await self.send(text_data=json.dumps({
                "type": "kicked",
                "username": "server",
                "message": "Вас удалили из чата"
            }))
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            await self.close()
