from django.shortcuts import render
from .models import Profile
from Common import security, constants
from django.http.response import HttpResponse
# Controller functions handle members actions and activities

def AddProfilePkey(request, userId):
    userProfile = Profile.objects.get(user_id = userId)
    userProfile.pkey = security.Encrypt(constants.USER_STRING, userId)
    userProfile.save()
    return HttpResponse('done')
def testDecrypt(request, temp):
    result1 = security.Decrypt(temp).decode("utf-8").split('_')
    return HttpResponse(result1[0]+'/n'+result1[1]+'/n'+result1[2])

'''
def member_search(request):
    if request.is_ajax():
        search_filter = ''
        if request.method == 'GET':
            search_filter = request.GET['member_search']
        
        condition = Q()
        if search_filter.isdigit():
            condition = Q(code=search_filter)
        else:
            condition = Q(user__last_name__icontains=search_filter) | Q(user__first_name__icontains=search_filter)

        search_result = Members.objects.filter(condition)
        return render(request, 'club/members/member_list.html', { 'search_result': search_result })
    else:
        raise Http404

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