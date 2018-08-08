from django.contrib import admin
from django.urls import path, include
from .views import DocCatMem, mohsenTest, Categories, MemberDocuments, Dashboard, Member, MemberFemale

urlpatterns = [
    path('doccatmem/<int:_id>/doc/<int:_cat>/', DocCatMem, name= 'doccatmem'), 
    #path('doccat/', DocCatMem, name='test'),
    path('test', mohsenTest, name = 'mohsenTest'),
    path('dashboard/', Dashboard, name='dashboard'),
    path('member/', Member, name='member'),
    path('memberfemale/<int:user_id>/', MemberFemale, name='memberfemale'),
    # React WebService for patientDocs
    path('doccategories', Categories, name='doccategories'),
    path('userdocs/<int:user_id>/', MemberDocuments, name='userdocs'),
]