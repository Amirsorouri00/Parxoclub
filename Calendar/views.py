from django.shortcuts import render
from Common.constants import CALENDAR_TABLE
from .utils import EventCalendar
import datetime
import calendar
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http import HttpResponse, JsonResponse, Http404
from django.template.loader import render_to_string


def Calendar(request):
    if not request.GET.get('day__gte', None):
        extra_context = CalendarMaker(request)
        #return HttpResponse(request.GET.get('day__gte', None)) 
        #return HttpResponse(extra_context['previous_month'])
        return render(request, 'calendar/calendar.html', { 
                'previous_month': extra_context['previous_month'],
                'next_month': extra_context['next_month'],
                'calendar' : extra_context['calendar'],
            })
    else:
        extra_context = CalendarMaker(request)
        html = render_to_string('calendar/calendar-after-sidenave-calendar-wrapper.html', { 
                'previous_month': extra_context['previous_month'],
                'next_month': extra_context['next_month'],
                'calendar' : extra_context['calendar'],
            })
        #content = JSONRenderer().render(html)
        data = {'form': html}
        return JsonResponse(data, safe=False)
# Create your views here.

def CalendarStringer(request):
    extra_context = CalendarMaker(request)
    html = render_to_string('calendar/calendar-after-sidenave-calendar-wrapper.html', { 
            'previous_month': extra_context['previous_month'],
            'next_month': extra_context['next_month'],
            'calendar' : extra_context['calendar'],
        })
    #content = JSONRenderer().render(html)
    data = {'form': html}
    return JsonResponse(data, safe=False)
    # extra_context = CalendarMaker(request)
    # #return HttpResponse(extra_context['previous_month'])
    # return render(request, 'calendar/calendar.html', { 
    #         'previous_month': extra_context['previous_month'],
    #         'next_month': extra_context['next_month'],
    #         'calendar' : extra_context['calendar'],
    #     })

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
    extra_context['calendar'] = mark_safe(html_calendar)
    #extra_context['calendar'] = mark_safe(CALENDAR_TABLE)
    return extra_context
