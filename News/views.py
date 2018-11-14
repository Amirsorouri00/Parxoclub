import os

from .models import News as NewsModel
from .templatetags.newsio import get_news_picture
from .serializer import NewsSerializer

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import translation
from django.utils.translation import get_language_bidi, ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, authentication_classes, \
    permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

import datetime



# Create your views here.
def handle_uploaded_news_files(record_id, files, extension):
    upload_path = settings.NEWS_UPLOAD_URL + '{}/'.format(record_id)
    if not os.path.isdir(upload_path):
        os.makedirs(upload_path)
    for imgfile in files:
        #(tempname, extension) = os.path.splitext(imgfile.name)
        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        #with open(upload_path + filename + extension, 'wb+') as destination:
        with open(upload_path + 'amir.png', 'wb+') as destination:
            for chunk in imgfile.chunks():
                destination.write(chunk)

def News(request):
    if request.method == 'POST':
        if request.is_ajax():
            return HttpResponse('wrong method ajax used')
        else:
            SPANISH_LANGUAGE_CODE = request.POST.get('language', None)
            if SPANISH_LANGUAGE_CODE: 
                translation.activate(SPANISH_LANGUAGE_CODE)
                return render(request, 'news/news.html', {'rtl': get_language_bidi(), 'Token':request.user, 'user_uuid': request.user.uuid_user.user_uuid.hex})
            else:
                raise Http404
    else:
        return render(request, 'news/news.html', {'rtl': get_language_bidi(), 'Token':request.user, 'user_uuid': request.user.uuid_user.user_uuid.hex})

@login_required(login_url="/authenticate/login/")
def AddNews(request):
    if request.method == 'POST':
        if request.is_ajax():
            files = request.FILES.getlist('photo')
            user = User.objects.get(username = request.user)
            news = NewsModel.objects.create(title = request.POST.get('title', None), description = request.POST.get('description', None), created_at = datetime.datetime.now(), user_created = user)
            with open(settings.FILE_UPLOAD_URL + 'news/' + news.news_uuid.news_uuid.hex, 'w') as f:
                myfile = File(f)
                myfile.write(request.POST.get('description', None))
                myfile.closed
                f.closed
            photo_name = request.POST.get('photo_name', False)
            uuid = user.uuid_user
            if uuid is None:
                return JsonResponse({
                    'modal': false, 
                    'notification': { 
                        'type': 'error',
                        'message': 'uuid is none.'
                    }
                })
            handle_uploaded_news_files(uuid.user_uuid.hex, files, photo_name)
            return JsonResponse({
                'modal': True, 
                'notification': { 
                    'type': 'success',
                    'message': 'Updated successfully.'
                }
            })
        else:
            return HttpResponse('wrong method')
    else:
        return HttpResponse('wrong method')


def GetNews(request):
    if request.method == 'POST':
        if request.is_ajax():
            return HttpResponse('wrong method')
        else:
            return HttpResponse('wrong method')
    else:
        if request.is_ajax():
            news = NewsModel.objects.all()
            news_serialized = NewsSerializer(news, many = True)
            json = {'data': news_serialized.data}
            content = JSONRenderer().render(json)
            return HttpResponse(content)
        else:
            return HttpResponse('wrong method')