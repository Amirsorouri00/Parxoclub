from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .views import DocCatMem, mohsenTest, Categories, MemberDocuments, Dashboard, Member, MemberFemale, SpecialistsHistory, TokenReturner, DocumentFilter, test

urlpatterns = [
    path('doccatmem/<int:_id>/doc/<int:_cat>/', DocCatMem, name= 'doccatmem'), 
    #path('doccat/', DocCatMem, name='test'),
    path('test', mohsenTest, name = 'mohsenTest'),
    path('dashboard/', Dashboard, name='dashboard'),
    path('member/', Member, name='member'),
    path('memberfemale/', MemberFemale, name='memberfemale'),
    path('gettoken/', TokenReturner, name='token_returner'),
    path('documentfilter/', ensure_csrf_cookie(DocumentFilter), name='document_filter'),
    path('test/', test, name='test'),
    # React WebService for patientDocs
    path('doccategories', Categories, name='doccategories'),
    path('specialists/history/', SpecialistsHistory, name='specialists_history'),
    path('userdocs/<int:user_id>/', MemberDocuments, name='userdocs'),
]