from django.urls import path, include
from .views import Calendar, EventTypes, AddEvents, GetOneEvent, GetDayEvents
from django.conf.urls import url
app_name = 'calendar'
urlpatterns = [
    #url(r'^(?P<day__gte>\d{4}-\d{2}-\d{2})/$', CalendarStringer, name='months_link'),
    path('eventtypes/', EventTypes),
    path('addevents/', AddEvents),
    path('', Calendar, name = 'calendar_get'),
    path('getoneevent/', GetOneEvent, name = 'get_one_events'),
    path('getdayevents/', GetDayEvents, name='get_day_events'),

    #path('admin/', admin.site.urls),
]