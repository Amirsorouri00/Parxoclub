from django.urls import path, include
from .views import AddProfilePkey, TestDecrypt, Login, LoginPageUsernameValidation, Logout, MemberSearch
from rest_framework.authtoken import views
from django.conf.urls import url
urlpatterns = [
    # Test
    #url(r'^(?P<temp>[^/]+)/$', TestDecrypt, name = 'testdec'),
    path('addprofilepk/<int:userId>/', AddProfilePkey, name = 'add_profile_pkey'),
    # Login
    path('login/', Login, name = 'login'),
    path('logout/', Logout, name = 'logout'),
    url(r'^validate_username/$', LoginPageUsernameValidation, name='validate_username'),
    url(r'^api-token-auth/', views.obtain_auth_token),
    path('search/', MemberSearch, name = 'mem_search'),


    #path('admin/', admin.site.urls),
]
