# Channel
from channels.exceptions import AcceptConnection, DenyConnection, InvalidChannelLayerError
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from . import consumer
from Common import security, constants
from .models import Room, RoomUsers, RoomMessages
from Log.chatlog import ConsumerLog
# Django
from django.db.models import Count

class ConsumerHandler():
    
    def CheckExistant(self, typeOf, sender_id, contact_or_room_id):  
        room_id = None
        if typeOf == constants.USER_CONTACT_HAVE_ROOM:
            room = RoomUsers.objects.values("room_id")\
            .filter(user_id__in=[sender_id, contact_or_room_id])\
            .annotate(room_count=Count("room_id"))\
            .filter(room_count=2)[:1]
            if room:
                room_id = room[0]['room_id']
                return room_id
            else: return None
        elif typeOf == constants.USER_EXIST_IN_ROOM:
            #print('checkAndaddmetoroom')
            result = RoomUsers.objects.filter(room_id = contact_or_room_id)\
                .filter(user_id__in = [sender_id])[:1]
            if result:
                return True
            else: return False

    #@transaction.atomic
    def CreateRoom(self, sender_id, contact_id):
        # Create new chat room 
        ConsumerLog('CreateRoom: ', True, ' hello')
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
        ConsumerLog('AddToRoom: ', True, ' hello')
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
        ConsumerLog('CreateRoomMessage: ', True, ' hello')
        roomMessages = RoomMessages.objects.create(message = Message, room_id = self.room_name, sender_id = self.sender_id)
        roomMessages.save()
    
    def ConnectHandler(self):
        ConsumerLog('ConnectHandler: ', True, ' hello')
        self.senderPrivateKey = self.scope['url_route']['kwargs']['senderprivatekey']
        temp = security.Decrypt(self.senderPrivateKey).decode("utf-8").split('_')
        sender_user_or_room = temp[0] 
        self.sender_id = temp[1]
        if sender_user_or_room == constants.ROOM_STRING:
            ConsumerLog('error,  ', True, ' hello')
            print('error')
            return None

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
            return room_id
        elif user_or_room == constants.ROOM_STRING:
            room_id = room_or_user_id
            exist_or_not = self.CheckExistant(constants.USER_EXIST_IN_ROOM, self.sender_id, room_id) #see
            if exist_or_not == False:
                result = self.AddToRoom(self.sender_id, room_id) #see
                if result == True: #see
                    print('good')
                    return room_id
                    #self.send({'message':'good'})
                else:
                    #return None
                    #print('error')
                    raise DenyConnection
            else: return room_id
        else:
            print('error')
            return None
            #raise DenyConnection
