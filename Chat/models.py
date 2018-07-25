from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime
# Create your models here.

class Room(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateField(default=datetime.date.today)
    label = models.SlugField(max_length=100)
    group = models.BooleanField(default=False)
    pkey = models.CharField(max_length=100, blank=False, null=False)
    def __unicode__(self):
        return self.label

class RoomUsers(models.Model):
    # Foreign Keys
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __unicode__(self):
        return self.label

class RoomMessages(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    # Foreign Keys
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __unicode__(self):
        return '[{timestamp}] {sender}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime("%H:%M").lstrip("0")#.replace(" 0", " ")
    
    def as_dict(self):
        return {'sender': self.sender.profile.pkey, 'message': self.message, 'timestamp': self.formatted_timestamp}