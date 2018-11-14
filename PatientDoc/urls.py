from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .views import DocumentPicHandler, HistoryCategoryService, GetUserHistory, DocCatMem, mohsenTest, Categories, ServiceCategories, MemberDocuments, ServiceMemberDocuments, Dashboard, Member, MemberFemale, SpecialistsHistory, TokenReturner, DocumentFilter, AddNewDocumentMemberPanel, EditDocumentMemberPanel, RemoveDocumentMemberPanel, AddMemberHistory, RemoveMemberHistory, test

urlpatterns = [ 
    #path('doccat/', DocCatMem, name='test'),
    path('test', mohsenTest, name = 'mohsenTest'),
    path('dashboard/', Dashboard, name='dashboard'),
    path('member/', Member, name='member'),
    path('memberfemale/', MemberFemale, name='memberfemale'),
    path('addnewdocmempanel/', ensure_csrf_cookie(AddNewDocumentMemberPanel), name='add_new_document_member_panel'),
    path('editdocmempanel/', ensure_csrf_cookie(EditDocumentMemberPanel), name='edit_document_member_panel'),
    path('adddochistory/', ensure_csrf_cookie(AddMemberHistory), name='add_document_member_history'),
    #path('editdochistory/', EditMemberHistory, name='edit_document_member_history'),
    path('removedochistory/', RemoveMemberHistory, name='remove_document_member_history'),
    path('getuserhistory/', ensure_csrf_cookie(GetUserHistory), name='get_user_history'),
    path('historycategory/', HistoryCategoryService, name='history_category'),
    path('removedocmempanel/', ensure_csrf_cookie(RemoveDocumentMemberPanel), name='remove_document_member_panel'),
    path('gettoken/', TokenReturner, name='token_returner'),
    path('documentfilter/', ensure_csrf_cookie(DocumentFilter), name='document_filter'),
    path('test/', test, name='test'),
    # React WebService for patientDocs
    path('doccategories', Categories, name='doccategories'),
    path('specialists/history/', SpecialistsHistory, name='specialists_history'),
    path('userdocs/<int:user_id>/', MemberDocuments, name='userdocs'),
    path('doccatmem/<int:_id>/doc/<int:_cat>/', DocCatMem, name= 'doccatmem'),
    path('getdocumentpic/', DocumentPicHandler, name= 'get_document_pic'),
    
    #path('doccatmem/<int:_id>/doc/<int:_cat>/', DocCatMem, name= 'doccatmem'),
    path('servicesubcatmenu/', ServiceCategories, name='service_sub_cat_menu'),
    path('servicememberdoc/', ServiceMemberDocuments, name= 'service_member_doc'),
    
]