import json
import datetime
# Channel
from channels.exceptions import AcceptConnection, DenyConnection, InvalidChannelLayerError
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
# Common
from Common import constants, security
# Log
from Log.chatlog import ConsumerLog
# Serializer
from .serializer import ChatMessageObject, ChatMessageObjectSerializer
# Handler
from .consumer_handler import ConsumerHandler

class ChatConsumer(AsyncJsonWebsocketConsumer, ConsumerHandler):

    async def connect(self):
        ConsumerLog('Connect: ', True, ' hello')
        room_id = self.ConnectHandler()
        self.room_name = room_id
        self.room_group_name = constants.CHAT_CONSUMER_PREFIX_GROUP_NAME % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        ConsumerLog('Disconnect: ', True, ' hello')
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        ConsumerLog('Data received at: ', True, '.../n Received: ', text_data, ' hello')
        text_data_json = json.loads(text_data)
        #cache.set('receive:after: '+text_data, 'hello', timeout=constants.CACHE_TTL)
        message = text_data_json['message']
        self.CreateRoomMessage(message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'ChatMessageSendToAll',
                'message': message
            }
        )

    # Receive message from room group
    async def ChatMessageSendToAll(self, event):
        message = event['message']
        chatMessage = ChatMessageObject('SendToAll', message, self.sender_id)
        chatMessageSerialized = ChatMessageObjectSerializer(chatMessage)
        #json = JSONRenderer().render(chatMessageSerialized.data)
        # Send message to WebSocket
        await self.send_json(chatMessageSerialized.data)
        # await self.send(text_data=json.dumps({
        #     'message': message
        # }))

