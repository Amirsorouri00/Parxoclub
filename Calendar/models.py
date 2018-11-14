# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from Common.models import SoftDeletionModel
from safedelete.models import SafeDeleteModel
from safedelete.models import HARD_DELETE_NOCASCADE, SOFT_DELETE, NO_DELETE
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from Common.constants import EVENT_TYPE_COLOR_CHOICES
# Create your models here.

class EventType(models.Model):
    #_safedelete_policy = NO_DELETE
    name = models.CharField(max_length=50)
    rtl_name = models.CharField(max_length=50, default='تایپ', blank=True, null=True)
    color = models.CharField(max_length = 10 ,choices = EVENT_TYPE_COLOR_CHOICES, blank = True, null = True)

class Event(models.Model):
    #_safedelete_policy = NO_DELETE
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True) #change to not nullable
    event_type =  models.ForeignKey(EventType, on_delete=models.PROTECT, blank=True, null=True)
    day_of_the_event = models.DateField(u'Day of the event', help_text=u'Day of the event')
    time_to_start_notifying = models.TimeField(u'Notifying time', help_text=u'Notifying time', blank=True, null=True)
    start_time = models.TimeField(u'Starting time', help_text=u'Starting time')
    end_time = models.TimeField(u'Final time', help_text=u'Final time')
    event_note = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)
    date_created = models.DateField()

    class Meta:
        verbose_name = u'Scheduling'
        verbose_name_plural = u'Scheduling'

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:    #edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end): #innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end: #outter limits
            overlap = True
        return overlap

    def get_absolute_url(self):
        url = reverse('calendar:get_one_events')
        # '''args=[self.id]'''
        return u'<a href="%s">%s</a>' % (url, str(self.start_time))

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Ending hour must be after the starting hour')

        events = Event.objects.filter(day=self.day)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
                    raise ValidationError(
                        'There is an overlap with another event: ' + str(event.day) + ', ' + str(
                            event.start_time) + '-' + str(event.end_time))
