from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('userchats/<int:userId>', views.UserChats, name = 'reactWholeChat'),
    url(r'^(?P<privatekey>[^/]+)/(?P<senderprivatekey>[^/]+)$', views.room, name='room'),
]