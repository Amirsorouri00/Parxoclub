from django.urls import path, include
from .views import Calender
from django.conf.urls import url
urlpatterns = [
    path('', Calender, name = 'login'),
    #path('admin/', admin.site.urls),
]