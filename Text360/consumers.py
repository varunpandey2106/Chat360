import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .templatetags.chatextras import initials
from django.utils.timesince import timesince

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name= self.scope['url_route']['kwargs']['room_name']
        self.room_group_name= f'chat_{self.room_name}'

        #join room group

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept() #accept is an asynchronous co-routine

    async def disconnect(self, close_code ):

        #leave room
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def recieve(self, text_data):

        #recieve msg from websocket frontend
        text_data_json=json.loads(text_data)
        type=text_data_json['type']
        message=text_data_json['message']
        name= text_data_json['name']
        agent=text_data_json.get('agent','')

        print('Recieve: ', type)

        if type == 'message':
            #send msg to room
            self.channel_layer.group_send(
                self.room_group_name,{
                    'type':'chat_message',
                    'message': message,
                    'name':name,
                    'agent':agent,
                    'initials':initials(name),
                    'created_at':'' #timesince(new_message.created_at)

                }
            )
    
    async def chat_message(self, event):
        #send message to websocket
        #built in function to async web socket consumer:
        await self.send(text_data=json.dumps({
            'type':event['type'],
            'message':event['message'],
            'name':event['name'],
            'agent':event['agent'],
            'initials':event['initials'],
            'created_at':event['created_at'],




        }))


