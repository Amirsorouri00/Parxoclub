from django.urls import path, include
from .views import Calendar
from django.conf.urls import url
app_name = 'calendar'
urlpatterns = [
    path('', Calendar, name = 'calendar_get'),
    #path('admin/', admin.site.urls),
]