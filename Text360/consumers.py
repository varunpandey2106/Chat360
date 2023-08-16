import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils.timesince import timesince
from django.http import JsonResponse
from .templatetags.chatextras import initials as calculate_initials
from  asgiref.sync import async_to_sync, sync_to_async
from .models import Room, Message
from home.models import Profile

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.get_room()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()  # accept is an asynchronous co-routine

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Receive msg from websocket frontend
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']
        name = text_data_json['name']
        agent = text_data_json.get('agent', '')

        print('Receive:', type)

        if type == 'message':
            new_message=await self.create_message(name,message, agent)
            # Send msg to room
            initials_value = await self.calculate_initials(name)
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'chat_message',
                    'message': message,
                    'name': name,
                    'agent': agent,
                    'initials': initials_value,
                    'created_at': timesince(new_message.created_at)
                }
            )

    async def chat_message(self, event):
        # Send message to websocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'name': event['name'],
            'agent': event['agent'],
            'initials': event['initials'],
            'created_at': event['created_at'],
        }))

    async def calculate_initials(self, name):
        return calculate_initials(name)


    @sync_to_async
    def get_room(self):
        self.room=Room.objects.get(uuid=self.room_name)
    
    @sync_to_async
    def create_message(self, sent_by,message, agent):
        message= Message.objects.create(body=message,sent_by=sent_by)

        if agent:
            message.created_by= Profile.objects.get(pk=agent )
            message.save()
        
        self.room.messages.add(message)

        return message
