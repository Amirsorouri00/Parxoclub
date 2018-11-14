from django.conf.urls import url
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

urlpatterns = [
    url(r'^$', views.index, name='chat'),
    path('userchats/<int:userId>/', views.UserChats, name = 'reactWholeChat'),
    path('chatpanel/', csrf_exempt(views.Chat), name = 'chat'),
    url(r'^(?P<privatekey>[^/]+)/(?P<senderprivatekey>[^/]+)$', views.room, name='room'),
]