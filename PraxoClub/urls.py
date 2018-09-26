"""PraxoClub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    #path('service/', include('WebService.urls')),
    path('chat/', include('Chat.urls')),
    path('authenticate/', include('Member.urls')),
    path('member/', include('Member.urls')),
    path('calendar/', include('Calendar.urls', namespace='calendar')),
    path('patientdoc/', include('PatientDoc.urls')),
     # path('admin/', admin.site.urls),
     # Ajax
    path('ajax/member/', include('Member.urls')),
    path('ajax/patientdoc/', include('PatientDoc.urls')),
]


urlpatterns += i18n_patterns (
    #path('service/', include('WebService.urls')),
    path('chat/', include('Chat.urls')),
    path('authenticate/', include('Member.urls')),
    path('member/', include('Member.urls')),
    path('calendar/', include('Calendar.urls', namespace='calendar2')),
    path('patientdoc/', include('PatientDoc.urls')),
     # path('admin/', admin.site.urls),
     # Ajax
    path('ajax/member/', include('Member.urls')),
    path('ajax/patientdoc/', include('PatientDoc.urls')),
)