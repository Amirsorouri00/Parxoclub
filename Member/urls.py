from django.urls import path, include
from .views import AddProfilePkey, TestDecrypt, Login, LoginPageUsernameValidation, Logout
from django.conf.urls import url
urlpatterns = [
    # Test
    #url(r'^(?P<temp>[^/]+)/$', TestDecrypt, name = 'testdec'),
    path('addprofilepk/<int:userId>/', AddProfilePkey, name = 'add_profile_pkey'),
    # Login
    path('login/', Login, name = 'login'),
    path('logout/', Logout, name = 'logout'),
    # Ajax
    url(r'^validate_username/$', LoginPageUsernameValidation, name='validate_username'),


    #path('admin/', admin.site.urls),
]
