from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import translation
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import BasicAuthentication, \
    SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, \
    permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

import json
from .models import Room, RoomUsers
from .serializer import RoomSerializer
from django.http import Http404
from django.http.response import HttpResponse


# Create your views here.

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, privatekey, senderprivatekey):
    return render(request, 'chat/room.html', {
        'privatekey': mark_safe(json.dumps(privatekey)),
        'senderprivatekey': mark_safe(json.dumps(senderprivatekey))
    })

def UserChats(request, userId):
    if request.is_ajax():
        room_ids = RoomUsers.objects.filter(user_id = userId)
        room_array = list()
        for ids in room_ids:
            result = getattr(ids, 'room_id')
            room_array.append(result)
        rooms = Room.objects.filter(id__in = room_array)
        roomSerialized = RoomSerializer(rooms, many = True)
        json = {'UserChats': roomSerialized.data}
        content = JSONRenderer().render(json)
        #return JsonResponse(json, safe=False)
        return HttpResponse(content)
# Create your views here.

@login_required(login_url="/authenticate/login/")
#@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
# @method_decorator(csrf_exempt, name='get')
# class Chat(View):
#     def get(request):
#         user = User.objects.get(username = request.user)
#         users = User.objects.all()
#         return render(request, 'chat/chats.html', {'user_id': user.id, 'users':users, 'rtl':translation.get_language_bidi()})
#     def post(request):
#         if request.is_ajax():
#             raise Http404
#         else:        
#             SPANISH_LANGUAGE_CODE = request.POST.get('language', None)
#             if SPANISH_LANGUAGE_CODE:
#                 translation.activate(SPANISH_LANGUAGE_CODE)
#                 extra_context = CalendarMaker(request)
#                 user = User.objects.get(username = request.user)
#                 users = User.objects.all()
#                 return render(request, 'chat/chats.html', {'user_id': user.id, 'users':users, 'rtl':translation.get_language_bidi()})
#             else: raise Http404
def Chat(request):
    if request.method == 'POST':
        if request.is_ajax():
            raise Http404
        else:        
            SPANISH_LANGUAGE_CODE = request.POST.get('language', None)
            if SPANISH_LANGUAGE_CODE:
                translation.activate(SPANISH_LANGUAGE_CODE)
                user = User.objects.get(username = request.user)
                users = User.objects.all()
                return render(request, 'chat/chats.html', {'user_id': user.uuid_user.user_uuid.hex, 'users':users, 'rtl':translation.get_language_bidi()})
            else: raise Http404
    else:
        user = User.objects.get(username = request.user)
        users = User.objects.all()
        return render(request, 'chat/chats.html', {'user_id': user.uuid_user.user_uuid.hex, 'users':users, 'rtl':translation.get_language_bidi()})


'''
def get_room_list(user_id):
    user_rooms = RoomUsers.objects.values_list('room_id').filter(user=user_id)
    # Performance challange on SQL IN clause
    room_list = RoomUsers.objects.filter(Q(room_id__in=user_rooms) & Q(user_id__ne=user_id))
    
    # room_list = RoomMessages.objects.values("room_id")\
    #             .filter(room__roomusers__user_id__ne=user_id)\
    #             .annotate(max_timestamp=Max("timestamp"))\
    #             .order_by("-max_timestamp")\
    #             .values("room__pkey", 
    #                 "room__roomusers__user_id", 
    #                 "room__roomusers__user__profile__pkey", 
    #                 "room__roomusers__user__first_name",
    #                 "room__roomusers__user__last_name")
                
    # json_room_list = JsonResponse({'results': list(room_list)})
    json_room_list = RoomMessages.objects.values("room_id")\
        .filter(room__roomusers__user_id__ne=user_id)\
        .annotate(max_timestamp=Max("timestamp"))\
        .order_by("-max_timestamp")\
        .values("room__pkey", 
                "room__roomusers__user_id", 
                "room__roomusers__user__profile__pkey", 
                "room__roomusers__user__first_name",
                "room__roomusers__user__last_name")
    json_room_list = serializers.serialize('json', list(json_room_list), fields=('room__pkey'))
    print ((json_room_list))
    # for room in json_room_list:
    #     print ("---------------")
    #     # room = room.replace(b'room__pkey',b'room_pkey')\
    #     #         .replace(b'room__roomusers__user_id',b'user_id')\
    #     #         .replace(b'room__roomusers__user__profile__pkey',b'user_pkey')\
    #     #         .replace(b'room__roomusers__user__first_name',b'user_firstname')\
    #     #         .replace(b'room__roomusers__user__last_name',b'user_lastname')
    #     print (room)


    return room_list

def chat(request):
    # For know i just search for peer rooms
    # later i must include group rooms
    room_list = get_room_list(request.user.id)

    return render(request, 'club/chat/index.html', { 
        'room_list': room_list,
        'contact_list': None 
    })

def chat_search(request):
    if request.is_ajax():
        if request.method == 'GET':
            user_id = request.user.id
            # Room list
            room_list = get_room_list(user_id)
            
            # Contact list
            search_filter = request.GET['chat_search']
            condition = Q(last_name__icontains=search_filter) | Q(first_name__icontains=search_filter)
            # Performance challange on "SQL IN" clause and Django "values_list" function
            condition = condition & ~Q(id=user_id) & ~Q(id__in=room_list.values_list('user_id'))
            contact_list = User.objects.filter(condition)
        
        return render(request, 'club/chat/list.html', { 
            'room_list': room_list,
            'contact_list': contact_list,
        })
    else:
        raise Http404

def chat_room(request, pkey):
    key_data = security.decrypt_pkey(pkey)
    id_type, id_value, id_suffixe = key_data.decode("utf-8").split('_')
    
    room_messages = None
    contact_user = None
    contact_room = None
    if id_type == consts.USER_ID_KEY:
        user_id = id_value
        contact_user = get_object_or_404(User, id=user_id)
    elif id_type == consts.ROOM_ID_KEY:
        room_id = id_value
        contact_room = get_object_or_404(ChatRoom, id=room_id)
        room_messages = RoomMessages.objects.filter(room_id=room_id).order_by('timestamp')
        if not contact_room.group:
            room_users = get_object_or_404(RoomUsers, Q(room_id=room_id) & ~Q(user_id=request.user.id))
            contact_user = room_users.user

    if request.is_ajax():
        
        return render(request, 'club/chat/room.html', { 
            'sender_pkey': request.user.profile.pkey,
            'contact_user': contact_user,
            'contact_room': contact_room,
            'room_messages': room_messages,
        })
    else:
        # For know i just search for peer rooms
        # later i must include group rooms
        room_list = get_room_list(request.user.id)


        return render(request, 'club/chat/index.html', { 
            'room_list': room_list,
            'contact_list': None,
            'sender_pkey': request.user.profile.pkey,
            'contact_user': contact_user,
            'contact_room': contact_room,
            'room_messages': room_messages, 
        })
'''