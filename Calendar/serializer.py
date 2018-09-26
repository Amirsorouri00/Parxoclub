# Rest_Framework
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers
# Models
from .models import Event, EventType
from django.contrib.auth.models import User

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ('name', 'color')

class EventSerializer(serializers.ModelSerializer):
    #membership_set = MembershipSerializer(read_only=True, many=True)
    event_type = serializers.CharField(source='event_type.name', read_only=True)
    class Meta:
        model = Event
        depth = 1
        fields = ('id', 'day_of_the_event', 'start_time', 'end_time', 'event_note', 'event_type')
        # , 'member_physician', 'member_user', 'member_profile'