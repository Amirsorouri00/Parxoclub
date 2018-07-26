import json
import datetime
# Channel
from channels.exceptions import AcceptConnection, DenyConnection, InvalidChannelLayerError
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
# Common
from Common import constants, security
# Models
from .models import Room, RoomUsers, RoomMessages
# Django
from django.db.models import Count
from django.core.cache import cache
from django.conf import settings
# Serializer
from .serializer import ChatMessageObject, ChatMessageObjectSerializer
# Rest_Framework
from rest_framework.renderers import JSONRenderer

class ChatConsumer(AsyncJsonWebsocketConsumer):

    def CheckExistant(self, typeOf, sender_id, contact_or_room_id):
        if typeOf == constants.USER_CONTACT_HAVE_ROOM:
            room = RoomUsers.objects.values("room_id")\
                .filter(user_id__in=[sender_id, contact_or_room_id])\
                .annotate(room_count=Count("room_id"))\
                .filter(room_count=2)[:1]
            room_id = None
            if room:
                room_id = room[0]['room_id']
            return room_id
        elif typeOf == constants.USER_EXIST_IN_ROOM:
            #print('checkAndaddmetoroom')
            result = RoomUsers.objects.filter(room_id = contact_or_room_id)\
                .filter(user_id__in = [sender_id])[:1]
            if result:
                return True
            else: return False
        else: return None

    #@transaction.atomic
    def CreateRoom(self, sender_id, contact_id):
        # Create new chat room 
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cache.set('CreateRoom: '+date, 'hello', timeout=constants.CACHE_TTL)
        chat_room = Room.objects.create(creator_id = sender_id,group=False)
        chat_room.save()
        room_id = chat_room.id
        chat_room.pkey = security.Encrypt(constants.ROOM_STRING, room_id)
        chat_room.save()
        # Add user in the room
        room_user = RoomUsers()
        room_user.room_id = room_id
        room_user.user_id = sender_id
        room_user.save()
        # Add contact in the room
        room_contact = RoomUsers()
        room_contact.room_id = room_id
        room_contact.user_id = contact_id
        room_contact.save() 
        return room_id

    def AddToRoom(self, sender_id, temp_room_id):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cache.set('AddToRoom: '+date, 'hello', timeout=constants.CACHE_TTL)
        room_user = None
        room_user = RoomUsers.objects.create(room_id = temp_room_id, user_id = sender_id)
        room_user.save()
        room = None
        room = Room.objects.all().update(group = True)

        if (room != None) & (room_user != None):
            return True
        else: 
            return False

    def CreateRoomMessage(self, Message):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cache.set('CreateRoomMessage: '+date, 'hello', timeout=constants.CACHE_TTL)
        roomMessages = RoomMessages.objects.create(message = Message, room_id = self.room_name, sender_id = self.sender_id)
        roomMessages.save()
        
    async def connect(self):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cache.set('Connect: '+date, 'hello', timeout=constants.CACHE_TTL)
        #self.room_name = self.scope['url_route']['kwargs']['room_name']
        #self.user_id = self.scope['url_route']['kwargs']['user_id']
        
        self.senderPrivateKey = self.scope['url_route']['kwargs']['senderprivatekey']
        temp = security.Decrypt(self.senderPrivateKey).decode("utf-8").split('_')
        sender_user_or_room = temp[0] 
        self.sender_id = temp[1]
        if sender_user_or_room == constants.ROOM_STRING:
            print('error')
            raise DenyConnection

        self.privateKey = self.scope['url_route']['kwargs']['privatekey']
        temp = security.Decrypt(self.privateKey).decode("utf-8").split('_')
        user_or_room = temp[0] 
        room_or_user_id = temp[1] 
        room_id = None

        if user_or_room == constants.USER_STRING:
            # No room Exist. id belongs to one of our users.
            contact_id = room_or_user_id
            #see
            room_id = self.CheckExistant(constants.USER_CONTACT_HAVE_ROOM, self.sender_id, contact_id) #see
            if room_id == None:
                room_id = self.CreateRoom(self.sender_id, contact_id) #see
            print('sdfsdf User')
        elif user_or_room == constants.ROOM_STRING:
            room_id = room_or_user_id
            exist_or_not = self.CheckExistant(constants.USER_EXIST_IN_ROOM, self.sender_id, room_id) #see
            if exist_or_not == False:
                result = self.AddToRoom(self.sender_id, room_id) #see
                if result == True: #see
                    print('good')
                    #self.send({'message':'good'})
                else:
                    #print('error')
                    raise DenyConnection
        else:
            print('error')
            #raise DenyConnection

        self.room_name = room_id
        self.room_group_name = constants.CHAT_CONSUMER_PREFIX_GROUP_NAME % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cache.set('Disconnect: '+date, 'hello', timeout=constants.CACHE_TTL)
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cache.set('received Data at: '+date+ '.../n Received: '+text_data, 'hello', timeout=constants.CACHE_TTL)
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

# Synchronous Tutorial Version

'''
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

# Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

'''