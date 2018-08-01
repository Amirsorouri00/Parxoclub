import datetime
# Rest_Framework
from rest_framework import serializers
# Models
from Member.models import Members
from .models import Room, RoomUsers, RoomMessages
from django.contrib.auth.models import User

class ChatMessageObject(object):
    def __init__(self, messageType, messsage, sender, *args):
        self.type = messageType
        self.message = messsage
        self.sender = sender
        self.created = datetime.datetime.now()
        # I have to add other Probable variable Here

class ChatMessageObjectSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=50)
    message = serializers.CharField(max_length=1000)
    sender = serializers.IntegerField()
    created = serializers.DateTimeField()

class ReplyMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMessages
        fields = ('id', 'message', 'timestamp', 'room')

class RoomMessagesSerializer(serializers.ModelSerializer):
    #sub_menu = serializers.StringRelatedField(many=True, allow_null=True)
    reply_to = ReplyMessageSerializer()
    class Meta:
        model = RoomMessages
        fields = ('id', 'message', 'timestamp', 'room', 'sender_id', 'reply_to')

class RoomUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomUsers
        fields = ('id', 'user_id')

class RoomSerializer(serializers.ModelSerializer):
    room_messages = RoomMessagesSerializer(many = True)
    room_users = RoomUsersSerializer(many = True)
    class Meta:
        model = Room
        fields = ('id', 'creator_id', 'created_at', 'label', 'group',
             'pk', 'room_messages', 'room_users')

