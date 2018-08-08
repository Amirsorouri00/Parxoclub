clu import os, datetime
# Django
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
# Models
from .models import DocCategories, Documents
from Member.models import Members, Memberships
# Rest_Framework
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import DocCatSubmenu
# Serializers
from .serializer import DocCategoriesSerializer, DocCategoriesSubMenuSerializer, DocumentsSerializer
from Member.serializer import MemberSerializer, UserSerializer
# Forms
from .forms import DocumentForm
# Create your views here.

#TODO list attache files should be concatenated with the json response
def list_atch_files(record_id):
    atch_files = None
    folder_path = settings.DOC_UPLOAD_URL + '{}/'.format(record_id)
    if os.path.isdir(folder_path):
        atch_files = os.listdir(folder_path)
    return atch_files

def handle_uploaded_doc_files(record_id, files):
    upload_path = settings.DOC_UPLOAD_URL + '{}/'.format(record_id)
    if not os.path.isdir(upload_path):
        os.makedirs(upload_path)
    for imgfile in files:
        (tempname, extension) = os.path.splitext(imgfile.name)
        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        with open(upload_path + filename + extension, 'wb+') as destination:
            for chunk in imgfile.chunks():
                destination.write(chunk)

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

def SpecialistsHistory(request):
    if request.is_ajax():
        cats = DocCategories.objects.all().order_by('index')
        catSerializer = DocCategoriesSerializer(cats, many=True)
        #return HttpResponse(catSerializer)
        json = {'DocCats': catSerializer.data}
        content = JSONRenderer().render(json)
        return HttpResponse(content)
    else:
        return Http404

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

def Dashboard(request):
    return render(request, 'patientdoc/dashboard.html')

def Member(request):
    return render(request, 'member/member.html')

def MemberFemale(request, user_id):
    return render(request, 'member/member-female.html')

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