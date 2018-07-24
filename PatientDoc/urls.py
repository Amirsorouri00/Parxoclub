from django.contrib import admin
from django.urls import path, include
from .views import DocCatMem, mohsenTest, Categories, DocsMem

urlpatterns = [
    path('doccatmem/<int:_id>/doc/<int:_cat>/', DocCatMem, name= 'doccatmem'),
    #path('doccat/', DocCatMem, name='test'),
    path('test', mohsenTest, name = 'mohsenTest'),
    path('doccategories', Categories, name='doccategories'),
    path('userdocs/<int:user_id>/', DocsMem, name='userdocs'),
]