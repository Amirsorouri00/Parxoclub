import datetime
# Rest_Framework
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
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