from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .views import News, AddNews, GetNews



urlpatterns = [ 

    path('getnews', GetNews, name='get_all_news'),
    path('add', AddNews, name = 'add_news'),    
    path('', News, name = 'news'),    
]