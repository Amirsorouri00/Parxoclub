from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<privatekey>[^/]+)/(?P<senderprivatekey>[^/]+)$', views.room, name='room'),
]