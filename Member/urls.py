from django.urls import path, include
from .views import UserPicHandler, ServiceLogout, CustomAuthToken, AddProfilePkey, TestDecrypt, Login, LoginPageUsernameValidation, Logout, MemberSearch, Maintenance, Validation, UpdateDjangoTemplateVariables, OneUserInfo, serializer_test, EditUser, RemoveUser, MemberSearchByPrefixx, AllUserInfo, ChangeUserPhoto
from rest_framework.authtoken import views
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    #url(r'^(?P<temp>[^/]+)/$', TestDecrypt, name = 'testdec'),
    path('addprofilepk/<int:userId>/', AddProfilePkey, name = 'add_profile_pkey'),
    # Login
    path('login/', Login, name = 'login'),
    path('logout/', Logout, name = 'logout'),
    url(r'^validate_username/$', Validation, name='validate_email'),
    path('maintenance/', Maintenance, name='maintenance'),
    path('oneuserinfo/', OneUserInfo, name='one_user_info'),
    path('alluserinfo/', AllUserInfo, name='all_user_info'),
    path('changeuserphoto/', ChangeUserPhoto, name='change_user_photo'),
    path('edituser/', EditUser, name='maintenance_edit_user'),
    path('removeuser/', RemoveUser, name='maintenance_remove_user'),
    path('search/', MemberSearch, name = 'mem_search'),
    path('prefixsearch/', MemberSearchByPrefixx, name = 'mem_prefix_search'),
    path('update/', UpdateDjangoTemplateVariables, name = 'update_variable'),
    path('', Login, name = 'login'),
    path('getuserpic/', UserPicHandler, name = 'get_user_pic'),

    url(r'^api-token-auth/', csrf_exempt(CustomAuthToken.as_view()), name='api_token_auth'),
    path('servicelogout/', ServiceLogout, name='service_logout'),
]
