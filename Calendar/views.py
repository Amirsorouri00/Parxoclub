from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, \
    get_supported_language_variant, ugettext_lazy as _
from khayyam import JalaliDate, JalaliDatetime, TehranTimezone

import datetime
from .forkedcalendar import Calendar, monthrange
from .models import Event, EventType
from .serializer import EventSerializer, EventTypeSerializer
from .utils import EventCalendar
from Calendar import forkedcalendar
from Common.constants import CALENDAR_TABLE
from django.http import Http404, HttpResponse, JsonResponse
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rtl import rtl
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers


success = {
    'modal': True, 
    'notification': { 
        'type': 'success',
        'message': 'Updated successfully.'
    }
}
error = {
    'modal': False, 
    'notification': { 
        'type': 'error',
        'message': 'user does not exist'
    }
}

def AddEvents(request):
    if request.is_ajax():
        if request.method == 'POST':
            event_type = request.POST.get('event_type', None)
            day_of_event = request.POST.get('date', None)
            try:
                if EventType.objects.get(name = event_type) is None:
                    event_type = EventType.objects.create(name = event_type, rtl_name = 'نیو تایپ', color = 'red')
                    event_type.save()
                else: event_type = EventType.objects.get(name = event_type)
            except ObjectDoesNotExist:
                event_type = EventType.objects.create(name = event_type, rtl_name = 'نیو تایپ', color = 'red')
                event_type.save()
            #language = get_supported_language_variant(get_language(), strict=False)
            language = request.POST.get('language', None)
            if language == 'en':
                try:
                    split_after_day = day_of_event.split('-')
                    d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=int(split_after_day[2]))
                except:
                    d = datetime.date.today()
            else:
                try:
                    split_after_day = day_of_event.split('-')
                    d = JalaliDate(year=int(split_after_day[0]), month=int(split_after_day[1]), day=int(split_after_day[2])).todate()
                except:
                    d = JalaliDate.today().todate()

            #title = request.POST.get('title', None)
            start_time = request.POST.get('start_time', None)
            end_time = request.POST.get('end_time', None)
            note = request.POST.get('event_note', None)
            new_event = Event.objects.create(user_id = request.POST.get('user_id', None), event_type_id = event_type.id, 
                day_of_the_event = d, start_time = start_time, end_time = end_time,
                event_note = note, date_created = datetime.date.today())
            new_event.save()
            return JsonResponse(success)
        else:
            raise Http404
    else:
        raise Http404
    

def EditEvents(request):
    if request.is_ajax():
        if request.method == 'POST':  
            #day_of_event = request.POST.get('date', None)
            #title = request.POST.get('date', None)
            start_time = request.POST.get('start_time', None)
            end_time = request.POST.get('end_time', None)
            note = request.POST.get('note', None)
            event = Event.objects.filter(id = request.POST.get('event_id', None))
            # if language == 'en':
            #     try:
            #         split_after_day = day_of_event.split('-')
            #         d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=int(split_after_day[2]))
            #     except:
            #         d = datetime.date.today()
            # else:
            #     try:
            #         split_after_day = day_of_event.split('-')
            #         d = JalaliDate(year=int(split_after_day[0]), month=int(split_after_day[1]), day=int(split_after_day[2])).todate()
            #     except:
            #         d = JalaliDate.today().todate()
            if event is not None:
                #event.day_of_the_event = date
                event.start_time = start_time
                event.end_time = end_time
                event.event_note = note
                event.save()
                return HttpResponse('Event Edited')
            else: 
                return HttpResponse('Event does not exist')
        else:
            raise Http404
    else:
        raise Http404

def RemoveEvents(request):  
    if request.is_ajax():
        if request.method == 'POST':
            event = Event.objects.filter(id = request.POST.get('event_id', None))
            if event:
                event.delete()
                return HttpResponse('Event Deleted')
            else: 
                return HttpResponse('Event does not exist')
        else:
            raise Http404
    else:
        raise Http404
    

def GetOneEvent(request):
    return HttpResponse('GetOneEvent')

def GetDayEvents(request):
    #return HttpResponse('GetDayEvents: '+ str(request.GET.get('month_val', None)))
    day_of_event = request.GET.get('month_val', None)
    language = get_supported_language_variant(get_language(), strict=False)
    if language == 'en':
        try:
            split_after_day = day_of_event.split('-')
            d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=int(split_after_day[2]))
        except:
            d = datetime.date.today()
    else:
        try:
            split_after_day = day_of_event.split('-')
            d = JalaliDate(year=int(split_after_day[0]), month=int(split_after_day[1]), day=int(split_after_day[2])).todate()
        except:
            d = JalaliDate.today().todate()
    events = Event.objects.filter(day_of_the_event__year=d.year)\
            .filter(day_of_the_event__month=d.month)\
            .filter(day_of_the_event__day=d.day)
    data = EventSerializer(events, many = True)
    json = {'events': data.data}
    content = JSONRenderer().render(json)
    return HttpResponse(content)
    return HttpResponse('GetDayEvents: '+ str(d))
    
def EventTypes(request):
    event_types = EventType.objects.all()
    data = EventTypeSerializer(event_types, many = True)
    json = {'types': data.data}
    content = JSONRenderer().render(json)
    return HttpResponse(content)

def Calendar(request):
    if request.method == 'POST':
        if request.is_ajax():
            raise Http404 #Must shows the correct error or be handled
        else:
            SPANISH_LANGUAGE_CODE = request.POST.get('language', None)
            if SPANISH_LANGUAGE_CODE is not None:
                translation.activate(SPANISH_LANGUAGE_CODE)
                extra_context = CalendarMaker(request)  
                today = datetime.date.today()
                today_event_list = Event.objects.filter(day_of_the_event = today)
                return render(request, 'calendar/calendar.html', { 
                        'previous_month': extra_context['previous_month'],
                        'event_panel_title': extra_context['event_panel_title'],
                        'next_month': extra_context['next_month'],
                        'month_title': extra_context['month_title'],
                        'month_value': extra_context['month_value'],
                        'calendar' : extra_context['calendar'],
                        'Token':request.user,
                        'today_event_list': today_event_list,
                        'rtl': translation.get_language_bidi()
                    })
            else: raise Http404 #Must shows the correct error
    else:
        if not request.GET.get('day__gte', None):
            extra_context = CalendarMaker(request)
            translation.activate(translation.get_language())
            today = datetime.date.today()
            today_event_list = Event.objects.filter(day_of_the_event = today)
            return render(request, 'calendar/calendar.html', { 
                    'previous_month': extra_context['previous_month'],
                    'event_panel_title': extra_context['event_panel_title'],
                    'next_month': extra_context['next_month'],
                    'month_title': extra_context['month_title'],
                    'month_value': extra_context['month_value'],
                    'calendar' : extra_context['calendar'],
                    'Token':request.user,
                    'today_event_list': today_event_list,
                    'rtl': translation.get_language_bidi()
                })
        else:
            extra_context = CalendarMaker(request)
            translation.activate(translation.get_language())
            html = render_to_string('calendar/calendar-after-sidenave-calendar-wrapper.html', { 
                    'previous_month': extra_context['previous_month'],
                    'event_panel_title': extra_context['event_panel_title'],
                    'next_month': extra_context['next_month'],
                    'month_title': extra_context['month_title'],
                    'month_value': extra_context['month_value'],
                    'calendar' : extra_context['calendar'],
                })
            data = {'form': html}
            return JsonResponse(data, safe=False)

def CalendarMaker(request):
    after_day = request.GET.get('day__gte', None)
    extra_context = {}
    language = get_supported_language_variant(get_language(), strict=False)
    get_date = None
    if not after_day:
        if language == 'fa' or translation.get_language_bidi():
            d = JalaliDate.today()
        else:
            d = datetime.date.today()
    else:
        try:
            split_after_day = after_day.split('-')
            if language == 'fa' or translation.get_language_bidi():
                d = JalaliDate(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
            else:
                d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
        except:
            if language == 'fa' or translation.get_language_bidi():
                d = JalaliDate.today()
            else:
                d = datetime.date.today()
    mydate = None
    julian = None
    if language == 'fa' or translation.get_language_bidi():
        # get_date = d
        # d = JalaliDate(d)
        julian = d.todate()
        mydate = JalaliDate
    else:
        #get_date = d
        julian = d
        mydate = datetime.date
    
    previous_month = mydate(year=d.year, month=d.month, day=1)  # find first day of current month
    previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
    previous_month = mydate(year=previous_month.year, month=previous_month.month,
                                    day=1)  # find first day of previous month

    last_day = monthrange(d.year, d.month)
    
    # tmp = forkedcalendar.Calendar()
    # tmp2 = tmp.monthdays2calendar(d.year+1, d.month+1)
    # return last_day, tmp2
    #return last_day
    # last_day = last_day[1]
    # if last_day == 31:
    #     last_day = 30
    next_month = mydate(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
    next_month = next_month + datetime.timedelta(days=1)  # forward a single day
    next_month = mydate(year=next_month.year, month=next_month.month, day=1)  # find first day of next month
    extra_context['previous_month'] = reverse('calendar:calendar_get') + '?day__gte=' + str(
        previous_month)
    extra_context['next_month'] = reverse('calendar:calendar_get') + '?day__gte=' + str(
        next_month)

    cal = EventCalendar()
    html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
    tmp = datetime.date(year = julian.year, month = julian.month, day = 1)
    #html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
    #extra_context['month_title'] = cal.month_title(d.year, d.month, withyear=True)
    extra_context['month_title'] = d.strftime('%Y %B %d')
    extra_context['event_panel_title'] = d.strftime('%Y %B')
    extra_context['month_today'] = ''+str(d.month)+' '+str(d.year) 
    extra_context['month_value'] = ''+str(d.year) +'-'+str(d.month)+'-'
    extra_context['calendar'] = mark_safe(html_calendar)
    #extra_context['calendar'] = mark_safe(CALENDAR_TABLE)
    return extra_context
