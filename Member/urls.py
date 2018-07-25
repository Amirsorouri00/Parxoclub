from django.urls import path, include
from .views import AddProfilePkey, testDecrypt
from django.conf.urls import url
urlpatterns = [
    path('addprofilepk/<int:userId>/', AddProfilePkey, name= 'add_profile_pkey'),
    url(r'^(?P<temp>[^/]+)/$', testDecrypt, name='testdec'),
     #path('admin/', admin.site.urls),
]
