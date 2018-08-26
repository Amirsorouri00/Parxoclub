from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.index, name='chat'),
    path('userchats/<int:userId>/', views.UserChats, name = 'reactWholeChat'),
    path('panel/', views.Chat, name = 'chat'),
    url(r'^(?P<privatekey>[^/]+)/(?P<senderprivatekey>[^/]+)$', views.room, name='room'),
]