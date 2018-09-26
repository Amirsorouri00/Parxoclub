from django.shortcuts import render
from Common.constants import CALENDAR_TABLE
from .utils import EventCalendar
import datetime
import calendar
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http import HttpResponse, JsonResponse, Http404
from django.template.loader import render_to_string
from .models import Event, EventType
from .serializer import EventTypeSerializer, EventSerializer
# Rest_Framework
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.utils import translation


def AddEvents(request):
    if request.is_ajax():
        if request.method == 'POST':
            date = request.POST.get('date', None)
            #title = request.POST.get('date', None)
            start_time = request.POST.get('start_time', None)
            end_time = request.POST.get('end_time', None)
            note = request.POST.get('note', None)
            new_event = Event.objects.create(user_id = 1, event_type_id = 2, 
                day_of_the_event = date, start_time = start_time, end_time = end_time,
                event_note = note)
            new_event.save()
            return HttpResponse(request.POST.get('date', None))
        else:
            raise Http404
    else:
        raise Http404
    

def EditEvents(request):
    if request.is_ajax():
        if request.method == 'POST':  
            date = request.POST.get('date', None)
            #title = request.POST.get('date', None)
            start_time = request.POST.get('start_time', None)
            end_time = request.POST.get('end_time', None)
            note = request.POST.get('note', None)
            event = Event.objects.filter(id = request.POST.get('event_id', None))
            if event:
                event.day_of_the_event = date
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
    try:
        split_after_day = day_of_event.split('-')
        d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=int(split_after_day[2]))
    except:
        d = datetime.date.today()
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
            if SPANISH_LANGUAGE_CODE:
                translation.activate(SPANISH_LANGUAGE_CODE)
                extra_context = CalendarMaker(request)  
                #return HttpResponse(request.GET.get('day__gte', None)) 
                #return HttpResponse(extra_context['previous_month'])
                return render(request, 'calendar/calendar.html', { 
                        'previous_month': extra_context['previous_month'],
                        'next_month': extra_context['next_month'],
                        'month_title': extra_context['month_title'],
                        'month_value': extra_context['month_value'],
                        'calendar' : extra_context['calendar'],
                        'rtl': translation.get_language_bidi()
                    })
            else: raise Http404 #Must shows the correct error or be handled
    else:
        if not request.GET.get('day__gte', None):
            extra_context = CalendarMaker(request)
            #return HttpResponse(request.GET.get('day__gte', None)) 
            #return HttpResponse(extra_context['previous_month'])
            return render(request, 'calendar/calendar.html', { 
                    'previous_month': extra_context['previous_month'],
                    'next_month': extra_context['next_month'],
                    'month_title': extra_context['month_title'],
                    'month_value': extra_context['month_value'],
                    'calendar' : extra_context['calendar'],
                    'rtl': translation.get_language_bidi()
                })
        else:
            extra_context = CalendarMaker(request)
            html = render_to_string('calendar/calendar-after-sidenave-calendar-wrapper.html', { 
                    'previous_month': extra_context['previous_month'],
                    'next_month': extra_context['next_month'],
                    'month_title': extra_context['month_title'],
                    'month_value': extra_context['month_value'],
                    'calendar' : extra_context['calendar'],
                })
            #content = JSONRenderer().render(html)
            data = {'form': html}
            return JsonResponse(data, safe=False)
# Create your views here.

def CalendarMaker(request):
    after_day = request.GET.get('day__gte', None)
    extra_context = {}

    if not after_day:
        d = datetime.date.today()
    else:
        try:
            split_after_day = after_day.split('-')
            d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
        except:
            d = datetime.date.today()

    previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
    previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
    previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                    day=1)  # find first day of previous month

    last_day = calendar.monthrange(d.year, d.month)
    next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
    next_month = next_month + datetime.timedelta(days=1)  # forward a single day
    next_month = datetime.date(year=next_month.year, month=next_month.month, day=1)  # find first day of next month
    extra_context['previous_month'] = reverse('calendar:calendar_get') + '?day__gte=' + str(
        previous_month)
    extra_context['next_month'] = reverse('calendar:calendar_get') + '?day__gte=' + str(
        next_month)

    cal = EventCalendar()
    html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
    #html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
    #extra_context['month_title'] = cal.month_title(d.year, d.month, withyear=True)
    extra_context['month_title'] = ''+str(d.month)+' '+str(d.year) 
    extra_context['month_value'] = ''+str(d.year) +'-'+str(d.month)+'-'
    extra_context['calendar'] = mark_safe(html_calendar)
    #extra_context['calendar'] = mark_safe(CALENDAR_TABLE)
    return extra_context
