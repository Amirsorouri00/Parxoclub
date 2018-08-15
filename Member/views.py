from .models import Profile
from django.http import Http404
from Common import security, constants
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.contrib.auth.models import User
from django.http import JsonResponse
# Rest_Framework
from rest_framework.renderers import JSONRenderer
from .serializer import UserSerializer
# Form
from .forms import UserForm, ProfileForm, MemberForm
# Controller functions handle members actions and activities

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
            request.session.set_expiry(3)
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

def Maintenance(request):
    #user = get_object_or_404(User, id=user_id)
    form_user = UserForm()
    form_profile = ProfileForm()
    form_member = MemberForm()
    #form_member = MembersForm(instance=user.members)
    return render(request, 'member/maintenance.html', { 
        'form_user': form_user,
        'form_profile': form_profile,
        'form_member': form_member,
    })
    #return render(request, 'member/maintenance.html')

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