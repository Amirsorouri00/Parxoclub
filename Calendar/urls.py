from django.urls import path, include
from .views import Calendar, CalendarStringer
from django.conf.urls import url
app_name = 'calendar'
urlpatterns = [
    url(r'^(?P<day__gte>\d{4}-\d{2}-\d{2})/$', CalendarStringer, name='months_link'),
    path('', Calendar, name = 'calendar_get'),
    #path('admin/', admin.site.urls),
]