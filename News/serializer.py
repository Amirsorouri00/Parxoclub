# Rest_Framework
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers

from django.contrib.auth.models import User
from django.core.files import File

import datetime
from datetime import timedelta
import time
from .models import News
import os



class NewsSerializer(serializers.ModelSerializer):
    #user = UserSerializer(read_only=True)
    class Meta:
        model = News
        fields = ('id' ,'title', 'description', 'created_at', 'user_created')