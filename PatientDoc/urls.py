from django.contrib import admin
from django.urls import path, include
from .views import DocCatMem, mohsenTest, Categories, MemberDocuments, Dashboard, Member, MemberFemale, SpecialistsHistory, test

urlpatterns = [
    path('doccatmem/<int:_id>/doc/<int:_cat>/', DocCatMem, name= 'doccatmem'), 
    #path('doccat/', DocCatMem, name='test'),
    path('test', mohsenTest, name = 'mohsenTest'),
    path('dashboard/', Dashboard, name='dashboard'),
    path('member/', Member, name='member'),
    path('memberfemale/', MemberFemale, name='memberfemale'),
    path('test/', test, name='test'),
    # React WebService for patientDocs
    path('doccategories', Categories, name='doccategories'),
    path('specialists/history/', SpecialistsHistory, name='specialists_history'),
    path('userdocs/<int:user_id>/', MemberDocuments, name='userdocs'),
]