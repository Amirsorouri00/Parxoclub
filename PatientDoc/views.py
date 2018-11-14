import os
from array import array

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import BasicAuthentication, \
    SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, authentication_classes, \
    permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

import datetime
from .forms import DocumentForm
from .models import DocCatSubmenu, DocCategories, Documents, HistoryCategory, PatientHistory
from .serializer import DocCategoriesSerializer, \
    DocCategoriesSubMenuSerializer, DocumentsSerializer, \
    MemberPanelDocumentsListSerializer, PatientHistorySerializer, GetUserHistorySerializer, OneUserHistorySerializer, \
    HistoryCategorySerializer
from Calendar.views import render_to_string
from Common.constants import LORE_IPSUM
from Member.models import Members, Memberships, UserUUID
from Member.serializer import MemberSerializer, TokenSerializer, \
    UserSerializer
from PatientDoc.serializer import SpecialistsHistoryObject, \
    SpecialistsHistorySerializer
from django.http import Http404, HttpResponse, JsonResponse
from django.utils.translation import get_language_bidi
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from rest_framework.authtoken.models import Token
from .templatetags.patientio import get_document_picture, get_all_document_pictures, document_pic_name

success = {
    'modal': True, 
    'notification': { 
        'type': 'success',
        'message': 'Updated successfully.'
    }
}
error = {
    'modal': False, 
    'notification': { 
        'type': 'error',
        'message': 'user does not exist'
    }
}
# Create your views here.

#TODO list attache files should be concatenated with the json response
def list_atch_files(record_id):
    atch_files = None
    folder_path = settings.DOC_UPLOAD_URL + '{}/'.format(record_id)
    if os.path.isdir(folder_path):
        atch_files = os.listdir(folder_path)
    return atch_files

def handle_uploaded_doc_files(user_id, record_id, files, extension):
    upload_path = settings.DOC_UPLOAD_URL + '{}/{}/'.format(user_id, record_id)
    if not os.path.isdir(upload_path):
        os.makedirs(upload_path)
    for imgfile in files:
        #(tempname, extension) = os.path.splitext(imgfile.name)
        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        with open(upload_path + filename + extension, 'wb+') as destination:
            for chunk in imgfile.chunks():
                destination.write(chunk)

# @api_view(['POST'])
# @authentication_classes((SessionAuthentication,))
# @permission_classes((IsAuthenticated,))
# @csrf_exempt   
def DocumentPicHandler(request):
    if request.is_ajax():
        if request.method == 'POST':
            user_uuid = request.POST.get('user_uuid', None)
            doc_uuid = request.POST.get('doc_uuid', None)
            name = request.POST.get('name', None)
            if name == '1':
                #return HttpResponse('name')
                #return HttpResponse(request.POST.get('name', None))
                names = document_pic_name(user_uuid, doc_uuid)
                return JsonResponse(names, safe=False)
            else:
                #return HttpResponse(request.POST.get('all', None))
                
                pictures = []
                if request.POST.get('all', None) == '1':
                    #return HttpResponse('all')
                    pictures = get_all_document_pictures(user_uuid, doc_uuid)
                else:
                    #return HttpResponse('not all')
                    filename = request.POST.get('file_name', None)
                    pictures = get_document_picture(user_uuid, doc_uuid, filename)
                return JsonResponse(pictures, safe=False)
        else:
            raise Http404
    else: raise Http404


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
@csrf_exempt
def TokenReturner(request):
    if request.is_ajax():
        username = request.user
        user = User.objects.get(username = username)
        user_token = Token.objects.get(user_id = user.id)
        user_token_serializer = TokenSerializer(user_token)
        json = {'Token': user_token_serializer.data}
        content = JSONRenderer().render(json)
        return HttpResponse(content)
    else:
        json = {'Token': 'Error'}
        content = JSONRenderer().render(json)
        return HttpResponse(content)

@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
@csrf_exempt    
def DocumentFilter(request):
    if request.is_ajax():
        # query must be based on request.user 
        # request.user returns username
        # Permission
        subfilter_or_filter = request.POST.get('sub_or_not', None)
        if subfilter_or_filter == 'submenu':
            title = request.POST.get('title', None)
            identifier = request.POST.get('id', None)
            submenu = DocCatSubmenu.objects.get(id = identifier)
            docs = Documents.objects.filter(doccatsubmenu = submenu, user_id = request.POST.get('user_id', None))
            if docs:    
                docSerializer = MemberPanelDocumentsListSerializer(docs, many=True)
                json = {'DocCats': docSerializer.data}
                content = JSONRenderer().render(json)
                return HttpResponse(content)
            else: return JsonResponse(error)
        elif subfilter_or_filter == 'menu':
            title = request.POST.get('title', None)
            identifier = request.POST.get('id', None)
            categorymenu = DocCategories.objects.get(id = identifier)
            docs = Documents.objects.filter(category = categorymenu, user_id = request.POST.get('user_id', None))
            if docs:
                docSerializer = MemberPanelDocumentsListSerializer(docs, many=True)
                json = {'DocCats': docSerializer.data}
                content = JSONRenderer().render(json)
                return HttpResponse(content) 
            else: return JsonResponse(error)
        else:
            raise Http404
    else:
        raise Http404


@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
@csrf_exempt  
def AddNewDocumentMemberPanel(request):
    # Documents must be queried based on document title and user_id
    # Permission
    if request.is_ajax():
        if request.method == 'POST':
            #handling whole images have been sent from client still remained(it is just a for...)
            files = request.FILES.getlist('photo_0', False)
            photo_name = request.POST.get('photo_0_name', False)
            category_index = request.POST.get('category_index', False) 
            item_index = request.POST.get('item_index', False) 
            user_id = request.POST.get('user_id', None)
            try:
                uuid = UserUUID.objects.get(user_id = user_id)
                category = DocCategories.objects.get(index = int(category_index))
                submenu = DocCatSubmenu.objects.get(index = int(item_index), docCategories_id = category.id)
                physician = User.objects.get(last_name = request.POST.get('supervisor', None))
            except ObjectDoesNotExist:
                uuid = None
                physician = None
                
            if uuid is None:
                return JsonResponse({
                    'modal': 'false', 
                    'notification': { 
                        'type': 'error',
                        'message': 'uuid or physician is none.'
                    }
                })
            document = Documents.objects.create(title = request.POST.get('title', None),
                        date = request.POST.get('date', None), comment = LORE_IPSUM, user_id = user_id,
                        doccatsubmenu_id = submenu.id, category_id = category.id, physician_id = physician.id, attachment = 1)
            document.save()
            handle_uploaded_doc_files(uuid.user_uuid.hex, document.uuid_document.document_uuid, files, photo_name)
            return JsonResponse({
                'modal': True, 
                'notification': { 
                    'type': 'success',
                    'message': 'Updated successfully.'
                }
            })
            #return HttpResponse(request.FILES)
        else:
            raise Http404
    else:
        raise Http404

@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
@csrf_exempt  
def EditDocumentMemberPanel(request):
    # Documents must be queried based on document title and user_id
    # Permission
    if request.is_ajax():
        if request.method == 'POST':
            #handling whole images have been sent from client still remained(it is just a for...)
            files = request.FILES.getlist('photo_0', False)
            photo_name = request.POST.get('photo_0_name', False)
            user_id = request.POST.get('user_id', None)
            try:
                uuid = UserUUID.objects.get(user_id = user_id)
                physician = User.objects.get(last_name = request.POST.get('supervisor', None))
                document = Documents.objects.get(id = request.POST.get('document_id', None), title = request.POST.get('title', None), user_id = user_id)
            except ObjectDoesNotExist:
                uuid = None
                physician = None

            if uuid is None:
                return JsonResponse({
                    'modal': false, 
                    'notification': { 
                        'type': 'error',
                        'message': 'uuid or physician or document is none.'
                    }
                })
            if physician and document and files:
                document.date = request.POST.get('date', None)
                document.physician_id = physician.id
                document.save()
                handle_uploaded_doc_files(uuid.user_uuid.hex, document.uuid_document.document_uuid, files, photo_name)
                #handle_uploaded_doc_files(document.pk+1000, files, photo_name)
                return JsonResponse({
                    'modal': True, 
                    'notification': { 
                        'type': 'success',
                        'message': 'Updated successfully.'
                    }
                })
            else: 
                return JsonResponse({
                    'modal': False, 
                    'notification': { 
                        'type': 'error',
                        'message': 'document and its dependencies does not exist',
                        'physician': physician.id,
                        'document': document.id,
                        'files': files
                    }
                })
        else:
            raise Http404
    else:
        raise Http404

@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
@csrf_exempt  
def RemoveDocumentMemberPanel(request):
    # Documents must be queried based on document title and user_id
    # Permission
    return HttpResponse('RemoveDocumentMemberPanel')
    if request.is_ajax():
        if request.method == 'POST':
            document = Documents.objects.filter(title = request.POST.get('title', None), user_id = request.POST.get('title', None))
            if document:
                document.delete()
                return JsonResponse({
                'modal': True, 
                'notification': { 
                    'type': 'success',
                    'message': 'Updated successfully.'
                }
                })
            else: 
                return JsonResponse({
                'modal': False, 
                'notification': { 
                    'type': 'error',
                    'message': 'document and its dependencies does not exist'
                }
                })
        else:
            raise Http404
    else:
        raise Http404

@api_view(['POST', 'GET'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def Categories(request):
    if request.is_ajax():
        cats = DocCategories.objects.all().order_by('index')
        catSerializer = DocCategoriesSerializer(cats, many=True)
        #return HttpResponse(catSerializer)
        json = {'DocCats': catSerializer.data}
        content = JSONRenderer().render(json)
        return HttpResponse(content)
    else:
        return Http404

@api_view(['POST', 'GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def ServiceCategories(request):
    if request.is_ajax():
        cats = DocCategories.objects.all().order_by('index')
        catSerializer = DocCategoriesSerializer(cats, many=True)
        #return HttpResponse(catSerializer)
        json = {'DocCats': catSerializer.data}
        content = JSONRenderer().render(json)
        return HttpResponse(content)
    else:
        return HttpResponse("content")

def SpecialistsHistory(request):
    # 127.0.0.1:8000/patientdoc/specialists/history/
    if request.is_ajax():
        query = Documents.objects.filter(user_id = 6)
        query2 = Documents.objects.filter(user_id = 6).values('physician_id').annotate(num=Count('physician_id'))
        arr = []
        for item in query:
            tmp = [x for x in query2 if x['physician_id']==item.physician.user_id]
            obj = SpecialistsHistoryObject(item.physician.prefix.name, item.physician.user.first_name, item.physician.user.last_name , item.physician.expertise.name, tmp[0]['num'])
            json = SpecialistsHistorySerializer(obj)
            content = JSONRenderer().render(json.data)
            if content not in arr:
                arr.append(content)
        content2 = JSONRenderer().render({'context': arr})
        return HttpResponse(content2)    
    else:
        return Http404


@api_view(['POST', 'GET'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def MemberDocuments(request, user_id):
    member_info = get_object_or_404(User, id=user_id)
    #cats = DocCategories.objects.all()
    docs = Documents.objects.filter(user_id=user_id).order_by('date')
    record_id = 0
    if docs:
        atch_files = list_atch_files(docs[0].id)

    if request.is_ajax():
        #catSerializer = DocCategoriesSerializer(cats)
        docSerializer = DocumentsSerializer(docs, many = True)
        memSerializer = UserSerializer(member_info)
        json = {'Docs': docSerializer.data,
            'MemberInfo': memSerializer.data}
        content = JSONRenderer().render(json)
        #return JsonResponse(json, safe=False)
        return HttpResponse(content) 
    else:
        raise Http404


@api_view(['POST', 'GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def ServiceMemberDocuments(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            member_info = get_object_or_404(User, username=request.user)
            #cats = DocCategories.objects.all()
            docs = Documents.objects.filter(user_id=member_info.id).order_by('date')
            record_id = 0
            if docs:
                atch_files = list_atch_files(docs[0].id)
        
            #catSerializer = DocCategoriesSerializer(cats)
            docSerializer = DocumentsSerializer(docs, many = True)
            memSerializer = UserSerializer(member_info)
            json = {'Docs': docSerializer.data,
                'MemberInfo': memSerializer.data}
            content = JSONRenderer().render(json)
            #return JsonResponse(json, safe=False)
            return HttpResponse(content) 
        else:
            return HttpResponse('Invalid User') 
    else:
        return HttpResponse('request must be the ajax type')

def Dashboard(request):
    rtl = get_language_bidi()
    return render(request, 'patientdoc/dashboard.html', {'rtl':rtl})

@login_required(login_url="/authenticate/login/")
def Member(request):
    if request.method == 'POST':
        if request.is_ajax():
            html = render_to_string('member/member-detail-history.html')
            #content = JSONRenderer().render(html)
            data = {'form': html}
            return JsonResponse(data, safe=False)
        else:
            SPANISH_LANGUAGE_CODE = request.POST.get('language', None)
            if SPANISH_LANGUAGE_CODE:    
                translation.activate(SPANISH_LANGUAGE_CODE)
                username = request.user
                user = User.objects.get(username = username)
                user_uuid = User.objects.get(username = request.user).uuid_user.user_uuid
                route_to_image = 'uploads/profilePics/'+ user_uuid.hex + '/' + 'amir.png'
                return render(request, 'member/member.html', {'rtl':get_language_bidi(), 'Token':username, 'user_uuid': user_uuid.hex})
            else:
                raise Http404
    else:
        user_uuid = User.objects.get(username = request.user).uuid_user.user_uuid
        route_to_image = 'uploads/profilePics/'+ user_uuid.hex + '/' + 'amir.png'
        return render(request, 'member/member.html', {'rtl':get_language_bidi(), 'Token':request.user, 'user_uuid': user_uuid.hex})

@login_required(login_url="/authenticate/login/")
def MemberFemale(request):
    if request.method == 'POST':
        if request.is_ajax():
            html = render_to_string('member/member-memberpanel-document-detail.html')
            #content = JSONRenderer().render(html)
            data = {'form': html}
            return JsonResponse(data, safe=False)
        else:
            raise Http404    
    else:
        rtl = get_language_bidi()
        username = request.user
        user = User.objects.get(username = username)
        return render(request, 'member/member.html', {'panel': 'panel', 'rtl':rtl, 'Token': user.auth_token})
        
def DocCatMem(request, _id, _cat):
    member_info = get_object_or_404(Members, user_id=_id)
    cats = DocCategories.objects.get(id=_cat)
    docs = Documents.objects.filter(user_id=_id, category_id=_cat).order_by('date')
    record_id = 0
    if docs:
        atch_files = list_atch_files(docs[0].id)
    if request.is_ajax():
        catSerializer = DocCategoriesSerializer(cats)
        docSerializer = DocumentsSerializer(docs, many = True)
        memSerializer = MemberSerializer(member_info)
        #return HttpResponse(memSerializer)
        json = {'DocCats': catSerializer.data, 'Docs': docSerializer.data,
            'MemberInfo': memSerializer.data}
        content = JSONRenderer().render(json)
        #return JsonResponse(json, safe=False)
        return HttpResponse(content) 
    else:
        raise Http404

def MemberHistoryDocument(request):
    if request.method == 'POST':
        if request.is_ajax():
            return HttpResponse('MemberHistoryDocument')
        else:
            raise Http404
    else:
        raise Http404

@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
@csrf_exempt
def AddMemberHistory(request):
    success = {
                'modal': True, 
                'notification': { 
                    'type': 'success',
                    'message': 'Updated successfully.'
                }
            }
    error = {
        'modal': False, 
        'notification': { 
            'type': 'error',
            'message': 'user does not exist'
        }
    }
    if request.method == 'POST':
        if request.is_ajax():
            #return HttpResponse(request.user())
            user, patient_history, history_category = [None, None, None]
            try:
                history_category = HistoryCategory.objects.filter(name = request.POST.get('title', None))[:1].get()
            except ObjectDoesNotExist:
                #Check index must be added
                history_category = HistoryCategory.objects.create(name = request.POST.get('title', None), rtl_name = 'فارسیه همین انگلیسیه')
                history_category.save()
            try:
                user = User.objects.get(username = request.user)
            except ObjectDoesNotExist:
                return JsonResponse(error)
            history = request.POST.get('history', None)
            try:
                patient_history = PatientHistory.objects.filter(user_id = user.id, category_id = history_category.id)[:1].get()
                patient_history.context = history
                patient_history.save()
            except ObjectDoesNotExist:
                patient_history = PatientHistory.objects.create(user_id = user.id, title = 'blob', context = history, category_id = history_category.id, user_created_id = user.id)
                patient_history.save()

            return JsonResponse(success)
        else:
            raise Http404
    else:
        raise Http404

@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
@csrf_exempt
def RemoveMemberHistory(request):
    if request.method == 'POST':
        if request.is_ajax():
            return HttpResponse('RemoveMemberHistory')
        else:
            raise Http404
    else:
        raise Http404

def HistoryCategoryService(request):
    if request.method == 'POST':
        if request.is_ajax():
            raise Http404
        else:
            raise Http404
    else:
        history_category = HistoryCategory.objects.all()
        history_category_serialize = HistoryCategorySerializer(history_category, many=True)
        json = {'data': history_category_serialize.data}
        content = JSONRenderer().render(json)
        return HttpResponse(content)


# @api_view(['POST'])
# @authentication_classes((SessionAuthentication, TokenAuthentication))
# @permission_classes((IsAuthenticated,))
# @csrf_exempt
def GetUserHistory(request):
    if request.method == 'POST':
        if request.is_ajax():
            #username = request.user
            user_id = request.POST.get('user_id', None)
            #user = User.objects.get(username = username)
            patient_histories = PatientHistory.objects.filter(user_id = user_id).values('category_id')            
            history_categories = HistoryCategory.objects.filter(id__in = patient_histories)
            history_categories_serialize = OneUserHistorySerializer(history_categories, many = True)
            json = {'data': history_categories_serialize.data}
            content = JSONRenderer().render(json)
            return HttpResponse(content)
            #return HttpResponse('GetUserHistory')
        else:
            raise Http404
    else:
        raise Http404

# returns response to the ajax request sending from template attachment tag
def record_atch(request, _id):
    atch_files = os.listdir(settings.DOC_UPLOAD_URL + '{}/'.format(_id))
    if request.is_ajax():
        return render(request, 'club/members/document/attachments.html', { 
            'record_id': _id,
            'atch_files': atch_files,
        })
    else:
        raise Http404

def document_create(request, _id, _cat=1):
    if request.is_ajax():
        if request.method == 'POST':
            form = DocumentForm(request.POST)
            if form.is_valid():
                files = request.FILES.getlist('files')
                # Create record
                new_doc = form.save(commit=False)
                new_doc.user_id = _id
                new_doc.category_id = _cat
                new_doc.attachment = len(files)
                new_doc.save()
                # Upload files 
                handle_uploaded_doc_files(new_doc.pk, files)
                return JsonResponse({
                    'modal': True, 
                    'notification': { 
                        'type': 'success',
                        'message': 'Document saved successfully.'
                    }
                })
            else:
                return render(request, 'club/members/document/form.html', { 
                    'form': form,
                    'member_id': _id,
                    'category_id': _cat,
                    'new_doc': True, 
                })
        else:
            form = DocumentForm()
            return render(request, 'club/members/document/form.html', { 
                'form': form,
                'member_id': _id,
                'category_id': _cat, 
                'new_doc': True, 
            })
    else:
        raise Http404

def mohsenTest(request):
    menuList = [
        # Laboratory & Pathology
        {   
            'id': 1, 
            'icon': 'lab', 
            'label': 'Laboratory & Pathology',
            'badge': 0, 
            'badgeColor': 'bg-yellow', 
            'submenu': [],
        },
        # Imaging
        {   
            'id': None, 
            'icon': 'imaging', 
            'label': 'Imaging',
            'badge': 0, 
            'badgeColor': 'bg-yellow',
            'submenu': [
                # Sonography
                {
                    'id': 2,
                    'label': 'Sonography', 
                },
                # MRI
                { 
                    'id': 3,
                    'label': 'MRI', 
                },
                # Radiology
                {
                    'id': 4, 
                    'label': 'Radiology', 
                },
            ],
        },
        # Heart
        {   
            'id': None, 
            'icon': 'heart', 
            'label': 'Heart', 
            'badge': 0, 
            'badgeColor': 'bg-yellow',
            'submenu': [
                # Electrocardiography
                { 
                    'id': 5, 
                    'label': 'Electrocardiography', 
                },
                # Echo
                { 
                    'id': 6, 
                    'label': 'Echo', 
                },
                # Fitness Test
                { 
                    'id': 7, 
                    'label': 'Fitness Test', 
                },
                # CTA Result
                { 
                    'id': 8, 
                    'label': 'CTA Result', 
                },
                # CTA Report
                { 
                    'id': 9, 
                    'label': 'CTA Report', 
                },
                # Angioplasty
                { 
                    'id': 10, 
                    'label': 'Angioplasty', 
                },
            ],
        },
        # Digestive System
        {   
            'id': None, 
            'icon': 'digestive', 
            'label': 'Digestive System', 
            'badge': 0, 
            'badgeColor': 'bg-yellow',
            'submenu': [
                # Endoscopy
                { 
                    'id': 11, 
                    'label': 'Endoscopy', 
                },
                # Colonoscopy
                { 
                    'id': 12, 
                    'label': 'Colonoscopy', 
                },
            ],
        },
        # Seperator
        {
            'label': 'Seperator',
        },
        # Prescriptions
        {   
            'id': 13, 
            'icon': 'presc', 
            'label': 'Prescriptions', 
            'badge': 0, 
            'badgeColor': 'bg-yellow', 
            'submenu': [],
        },
        # Hospitalization
        {   
            'id': 14, 
            'icon': 'hospital', 
            'label': 'Hospitalization', 
            'badge': 0, 
            'badgeColor': 'bg-yellow', 
            'submenu': [],
        },
        # Medicinal schedule
        {   
            'id': 15, 
            'icon': 'medic', 
            'label': 'Medicinal schedule', 
            'badge': 0, 
            'badgeColor': 'bg-yellow', 
            'submenu': [],
        },
    ]
    content = JSONRenderer().render(menuList)
    #return JsonResponse(json, safe=False)
    return HttpResponse(content)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def test(request):
    if request.is_ajax():
        docs = Documents.objects.all()
        docSerializer = MemberPanelDocumentsListSerializer(docs, many=True)
        json = {'DocCats': docSerializer.data}
        content = JSONRenderer().render(json)
        return HttpResponse(content) 
    else:
        raise Http404

'''
def document_update(request, record_id):
    record_instance = get_object_or_404(Documents, id=record_id)
    atch_files = list_atch_files(record_id)
    if request.is_ajax():
        if request.method == 'POST':
            form = DocumentForm(request.POST, instance=record_instance)
            if form.is_valid():
                # Delete requested files 
                delete_files = request.POST.getlist('delete_files')
                for filename in delete_files:
                    delete_uploaded_doc_file(record_id, filename)
                # Upload files 
                files = request.FILES.getlist('files')
                handle_uploaded_doc_files(record_id, files)
                # Update record
                update_doc = form.save(commit=False)
                update_doc.attachment = update_doc.attachment - len(delete_files) + len(files)
                update_doc.save()
                
                return JsonResponse({
                    'modal': True, 
                    'notification': { 
                        'type': 'success',
                        'message': 'Document saved successfully.'
                    }
                })
            else:
                return render(request, 'club/members/document/form.html', { 
                    'form': form,
                    'member_id': record_instance.user.id,
                    'category_id': record_instance.category.id,
                    'record_id': record_id,
                    'atch_files': atch_files,
                })
        else:
            form = DocumentForm(instance=record_instance)
            return render(request, 'club/members/document/form.html', { 
                'form': form,
                'member_id': record_instance.user.id,
                'category_id': record_instance.category.id, 
                'record_id': record_id,
                'atch_files': atch_files,
            })
    else:
        raise Http404

def document_delete(request, record_id):
    category_record = get_object_or_404(Documents, id=record_id)
    if request.is_ajax():
        if request.method == 'POST':
            if category_record:
                # Delete record
                category_record.delete()
                # Delete files 
                delete_record_files(record_id)
                
                return JsonResponse({
                    'modal': True, 
                    'notification': { 
                        'type': 'success',
                        'message': 'Document deleted successfully.'
                    }
                })
            else:
                raise Http404
        else:
            return render(request, 'club/members/document/delete.html', { 
                'category_record': category_record, 
            })
    else:
        raise Http404
'''