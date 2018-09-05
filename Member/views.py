import datetime
from .models import Profile, Members
from django.http import Http404
from Common import security, constants
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db import connection
from django.contrib.auth.hashers import make_password
# Rest_Framework
from rest_framework.renderers import JSONRenderer
from .serializer import UserSerializer, MaintenanceUsersSerializer, MemberSerializer
from django.core import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Form
from .forms import UserForm, ProfileForm, MemberForm
# Controller functions handle members actions and activities
from collections import namedtuple
from PatientDoc.views import handle_uploaded_doc_files

def Maintenance(request):
    #user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        files = request.FILES.getlist('photo')
        user = User.objects.create(password = make_password(123456, salt=None, hasher='default'),
                is_superuser = 1, username = request.POST.get('first_name', None),
                first_name = request.POST.get('first_name', None),
                last_name = request.POST.get('last_name', None),
                email = request.POST.get('email', None), is_staff = 1, is_active = 1,
                date_joined = datetime.datetime.now())
        user.save()
        profile = Profile.objects.create(user_id = user.id, birthdate = request.POST.get('birthdate', None),
                gender = 1, mobile = request.POST.get('mobile', None),
                address = request.POST.get('address', None))
        profile.save()
        member = Members.objects.create(code = request.POST.get('code', None), user_id = user.id, membership_id = 1, physician_id = 1, Profile_id = 1)
        member.save()
        photo_name = request.POST.get('photo_name', False)
        handle_uploaded_doc_files(user.pk, files, photo_name)
        return JsonResponse({
            'modal': True, 
            'notification': { 
                'type': 'success',
                'message': 'Updated successfully.'
            }
        })
    else:
        return render(request, 'member/maintenance.html')

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def AddProfilePkey(request, userId):
    userProfile = Profile.objects.get(user_id = userId)
    userProfile.pkey = security.Encrypt(constants.USER_STRING, userId)
    userProfile.save()
    return HttpResponse('done')

def TestDecrypt(request, temp):
    result1 = security.Decrypt(temp).decode("utf-8").split('_')
    return HttpResponse(result1[0]+'/n'+result1[1]+'/n'+result1[2])

def Login(request):
    if request.user.is_authenticated:
        return HttpResponse('already login')
    elif request.method == 'POST':
        #nextURL = request.POST.get(REDIRECT_FIELD_NAME, '/')
        # user = User.objects.get(username = request.POST['username'])
        # user.set_password(request.POST['password'])
        # user.save()
        #next_url = request.POST.get('context', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user2 = authenticate(username=username, password=password)
        if user2 is not None:
            request.session.set_expiry(100000)
            login(request, user2)
            data = {
                'logged_in': True,
                'Error': None,
                'context': '/patientdoc/dashboard/'
            }
            return JsonResponse(data)
            #return redirect(nextURL)
        else:
            data = {
                'logged_in': False,
                'Error': None,
                'context': '/authenticate/logout/'
            }
            return JsonResponse(data)
    else:
        context = { REDIRECT_FIELD_NAME: request.GET.get(REDIRECT_FIELD_NAME, '/')}
        return render(request, 'member/login.html', context)

def LoginPageUsernameValidation(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)

def Logout(request):
    if request.user.is_authenticated == False:
        return HttpResponse('already loggedout')
    logout(request)
    #return HttpResponse('logged out')

def MemberSearch(request):
    if request.is_ajax():
        search_filter = ''
        if request.method == 'GET':
            search_filter = request.GET['member_search']
        
        condition = Q()
        if search_filter.isdigit():
            condition = Q(code=search_filter)
        else:
            condition = Q(last_name__icontains=search_filter) | Q(first_name__icontains=search_filter)

        data = UserSerializer(User.objects.filter(condition), many = True)
        json = {'users': data.data}
        content = JSONRenderer().render(json)
        search_result = {
            'users': User.objects.filter(condition)
        }
        #return JsonResponse(search_result)
        return HttpResponse(content)
    else:
        raise Http404

def MemberSearchByPrefixx(request):
    if request.is_ajax():
        search_filter = ''
        search_filter = request.POST.get('member_search', None)
        condition = Q()
        condition = Q(name__iexact=search_filter)
        cursor = connection.cursor()
        cursor.execute("SELECT auth_user.first_name as first_name, auth_user.last_name as last_name, member_prefixes.name as prefix_name, member_expertises.name as expertise_name \
                    FROM member_members join auth_user on auth_user.id = member_members.user_id \
                    join member_physicians on member_members.physician_id = member_physicians.user_id \
                    join member_prefixes on member_physicians.prefix_id = member_prefixes.id \
                    join member_expertises on member_physicians.expertise_id = member_expertises.id \
                    where member_prefixes.name = %s", ['Doctor'])
        results = namedtuplefetchall(cursor)
        #data = serializers.serialize('json', members, fields=('__all__'))
        return JsonResponse(results, safe=False)
        data = UserSerializer(members.objects.physician.prefix.filter(condition), many = True)
        json = {'users': data.data}
        content = JSONRenderer().render(json)
        search_result = {
            'users': User.objects.filter(condition)
        }
        #return JsonResponse(search_result)
        return HttpResponse(content)
    else:raise Http404

# def Maintenance(request):
#     #user = get_object_or_404(User, id=user_id)
#     if request.method == 'POST':
#         form_user = UserForm(request.POST)
#         form_profile = ProfileForm(request.POST)
#         form_member = MemberForm(request.POST)
#         if form_user.is_valid() & form_profile.is_valid() & form_member.is_valid():
#             form_user.save()
#             form_profile.save()
#             form_member.save()
#             return JsonResponse({
#                 'modal': True, 
#                 'notification': { 
#                     'type': 'success',
#                     'message': 'Updated successfully.'
#                 }
#             })
#         else:
#             html = render_to_string('member/maintenance.html', {'form_user': form_user,
#                 'form_profile': form_profile,
#                 'form_member': form_member,})
#             #content = JSONRenderer().render(html)
#             data = {'form': html, 'field':request.POST.get('field', None)}
#             return JsonResponse(data, safe=False)
#             # return render(request, 'member/maintenance.html', { 
#             #     #see (what about the error)
#             #     'form_user': form_user,
#             #     'form_profile': form_profile,
#             #     'form_member': form_member, 
#             # })
        
#     else:
#         form_user = UserForm()
#         form_profile = ProfileForm()
#         form_member = MemberForm()
#         Users = User.objects.all()
#         #form_member = MembersForm(instance=user.members)
#         return render(request, 'member/maintenance.html', { 
#             'form_user': form_user,
#             'form_profile': form_profile,
#             'form_member': form_member,
#         })
#     #return render(request, 'member/maintenance.html')

def Validation(request):
    value = request.POST.get('value', None)
    field = request.POST.get('field', None)
    if field == 'email':
        data = {
            'is_taken': User.objects.filter(email__iexact=value).exists(),
            'field': 'email',
        }
        if data['is_taken']:
            data['error'] = 'A user with this email already exists.'
    elif field == 'birthdate':
        data = {
            'is_taken': 'NONE',
            'field': 'birthdate',
        }
        form_profile = ProfileForm({'birthdate':value})
        data['error'] = form_profile.errors['birthdate'][0]
    else: data = {
            'is_taken': 'NONE'
        }
    return JsonResponse(data)

def UpdateDjangoTemplateVariables(request):
    #product_list = request.POST.get('email', None)
    data = {
        'error': request.POST.get('error', None),
    }
    html = render_to_string('common/common-field-error-message.html', {'variable':data})
    #content = JSONRenderer().render(html)
    data = {'form': html, 'field':request.POST.get('field', None)}
    return JsonResponse(data, safe=False)
    #return JsonResponse(content, safe=False)

def AllUserInfo(request):
    if request.is_ajax():
        user = User.objects.all()
        userSerializer = MaintenanceUsersSerializer(user, many = True)
        json = {'users': userSerializer.data}
        content = JSONRenderer().render(json)
        return HttpResponse(content)
    else:
        return Http404

def OneUserInfo(request):
    if request.is_ajax():
        #return HttpResponse('content')
        userId = request.POST.get('user_id', None)
        user = User.objects.get(id = userId)
        userSerializer = MaintenanceUsersSerializer(user)
        json = {'user': userSerializer.data, 'id': user.id}
        content = JSONRenderer().render(json)
        return HttpResponse(content)
    else:
        return Http404

def serializer_test(request):
    if request.is_ajax():
        #return HttpResponse('content')
        userId = request.POST.get('id', None)
        user = Members.objects.get(user_id = userId)
        userSerializer = MemberSerializer(user)
        json = {'user': userSerializer.data, 'url': '{% url "maintenance_edit_user" %}'}
        content = JSONRenderer().render(json)
        return HttpResponse(content)
    else:
        return Http404

def EditUser(request):
    if request.is_ajax():
        if request.method == 'POST':  
            user = User.objects.get(pk = request.POST.get('user_id', None))
            user.first_name = request.POST.get('first_name', None)
            user.last_name = request.POST.get('last_name', None)
            user.email = request.POST.get('email', None)
            user.save()
            profile = Profile.objects.get(pk = request.POST.get('user_id', None))
            profile.mobile = request.POST.get('mobile', None)
            profile.address = request.POST.get('address', None)
            profile.birthdate = request.POST.get('birthdate', None)
            profile.save()
            member = Members.objects.get(pk = request.POST.get('user_id', None))
            member.code = request.POST.get('code', None)
            member.save()
            files = request.FILES.getlist('photo')
            photo_name = request.POST.get('photo_name', False)
            handle_uploaded_doc_files(user.pk, files, photo_name)
            return JsonResponse({
                'modal': True, 
                'notification': { 
                    'type': 'success',
                    'message': 'Updated successfully.'
                }
            })
        else:
            return render(request, 'member/maintenance.html')
    else:
        return Http404

def RemoveUser(request):
    if request.is_ajax():
        if request.method == 'POST':  
            user = User.objects.get(pk = request.POST.get('user_id', None))
            profile = Profile.objects.get(pk = request.POST.get('user_id', None))
            member = Members.objects.get(pk = request.POST.get('user_id', None))
            #physician = physician.objects.get(pk = request.POST.get('user_id', None))
            #physician.delete()
            member.delete()
            profile.delete()
            user.delete()
            return JsonResponse({
                'modal': True, 
                'notification': { 
                    'type': 'success',
                    'message': 'Updated successfully.'
                }
            })
        else:
            return HttpResponse('request methode is get, it should be post')
    else:
        return Http404


'''
@transaction.atomic
def member_update(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.is_ajax():
        if request.method == 'POST':
            form_user = UserForm(request.POST, instance=user)
            form_profile = ProfileForm(request.POST, instance=user.profile)
            form_member = MembersForm(request.POST, instance=user.members)
            if form_user.is_valid() & form_profile.is_valid() & form_member.is_valid():
                form_user.save()
                form_profile.save()
                form_member.save()
                return JsonResponse({
                    'modal': True, 
                    'notification': { 
                        'type': 'success',
                        'message': 'Updated successfully.'
                    }
                })
            else:
                return render(request, 'club/members/member_update.html', { 
                    #see (what about the error)
                    'user': user, 
                    'form_user': form_user,
                    'form_profile': form_profile,
                    'form_member': form_member, 
                })
        else:
            form_user = UserForm(instance=user)
            form_profile = ProfileForm(instance=user.profile)
            form_member = MembersForm(instance=user.members)
            return render(request, 'club/members/member_update.html', { 
                'user': user, 
                'form_user': form_user,
                'form_profile': form_profile,
                'form_member': form_member,
            })
    else:
        raise Http404

def profile_photo(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    default_photo = not os.path.isfile(settings.PIC_UPLOAD_URL + user_id)
    if request.is_ajax():
        if request.method == 'POST':
            form_profile_photo = ProfilePhotoForm(request.POST, instance=profile)
            if form_profile_photo.is_valid():
                file_source = request.FILES.get('photo_source', False)
                file_blob = request.FILES.get('photo_blob', False)
                if file_blob:
                    handle_uploaded_photo(user_id, file_source, file_blob) 
                else:
                    delete_uploaded_photo(user_id)
                form_profile_photo.save()
                return JsonResponse({
                    'modal': True, 
                    'notification': { 
                        'type': 'success',
                        'message': 'Profile photo changed successfully.'
                    }
                })
            else:
                return render(request, 'club/profile_photo.html', { 
                    'form_profile_photo': form_profile_photo,
                    'user_id': user_id,
                    'default_photo': default_photo,
                })
        else:
            form_profile_photo = ProfilePhotoForm(instance=profile)
            return render(request, 'club/profile_photo.html', { 
                'form_profile_photo': form_profile_photo,
                'user_id': user_id,
                'default_photo': default_photo,
            })
    else:
        raise Http404
'''