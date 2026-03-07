import json
from channels.generic.websocket import AsyncWebsocketConsumer
from Chat.models import *
from channels.db import sync_to_async

class PingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        await self.send(text_data=json.dumps({
            "type": "info",
            "message": "Connected!!"
        }))

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        data = json.loads(text_data)
        msg = data.get("message", "")

        #reciprocate
        await self.send(text_data=json.dumps({
            "type": "message",
            "message": f"{msg} "
        }))

    async def disconnect(self, close_code):
        pass

class ChatConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def create_message(self, chat_id, text):
        chat = Chat.objects.get(id=chat_id)
        message = Message.objects.create(chat=chat, text=text)
        return {
            "id": message.id,
            "chat_id": chat_id,
            "text": text
        }


    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f"chat_{self.chat_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()


    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        data = json.loads(text_data)
        message = data.get("message", "")

        if not message:
            return
        await self.channel_layer.group_send(self.room_group_name, {"type": "chat.message", "message": message})
        await self.create_message(self.chat_id, message)

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
