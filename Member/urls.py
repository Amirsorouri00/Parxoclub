from django.urls import path, include
from .views import AddProfilePkey, TestDecrypt, Login
from django.conf.urls import url
urlpatterns = [
    path('addprofilepk/<int:userId>/', AddProfilePkey, name = 'add_profile_pkey'),
    path('', Login, name = 'login'),
    url(r'^(?P<temp>[^/]+)/$', TestDecrypt, name = 'testdec'),
     #path('admin/', admin.site.urls),
]
