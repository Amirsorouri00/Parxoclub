from django.urls import path, include
from .views import AddProfilePkey, TestDecrypt, Login, LoginPageUsernameValidation, Logout, MemberSearch, Maintenance, Validation, UpdateDjangoTemplateVariables, OneUserInfo, serializer_test, EditUser, RemoveUser, MemberSearchByPrefixx
from rest_framework.authtoken import views
from django.conf.urls import url
urlpatterns = [
    # Test
    #url(r'^(?P<temp>[^/]+)/$', TestDecrypt, name = 'testdec'),
    path('addprofilepk/<int:userId>/', AddProfilePkey, name = 'add_profile_pkey'),
    # Login
    path('login/', Login, name = 'login'),
    path('logout/', Logout, name = 'logout'),
    url(r'^validate_username/$', Validation, name='validate_email'),
    path('maintenance/', Maintenance, name='maintenance'),
    path('oneuserinfo/', OneUserInfo, name='one_user_info'),
    path('edituser/', EditUser, name='maintenance_edit_user'),
    path('removeuser/', RemoveUser, name='maintenance_remove_user'),
    url(r'^api-token-auth/', views.obtain_auth_token),
    path('search/', MemberSearch, name = 'mem_search'),
    path('prefixsearch/', MemberSearchByPrefixx, name = 'mem_prefix_search'),
    path('update/', UpdateDjangoTemplateVariables, name = 'update_variable'),

    #path('admin/', admin.site.urls),
]
