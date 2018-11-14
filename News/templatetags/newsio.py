import os, glob, base64
from django import template
from django.conf import settings

register = template.Library()

news_pictures_path = settings.NEWS_UPLOAD_URL
news_default_pic = settings.STATIC_ROOT + 'img/fileNotFound.svg'

@register.simple_tag
def news_pic_name(user_uuid = "", news_uuid = ""):
    news_path = news_pictures_path + '{}/{}'.format(user_uuid, news_uuid)
    file_names = []
    if os.path.isdir(news_path) is False:
        info = os.stat(news_default_pic)
        data = {'name': 'filename', 'size': info.st_size}
        file_names.append(data)
    else:
        for filename in os.listdir(news_path):
            info = os.stat(news_path + '/' + filename)
            print(info.st_mtime)
            print(info.st_size)
            data = {'name': filename, 'size': info.st_size}
            file_names.append(data)
    # with open("./common" + file_path, "rb") as image_file:
    #     encoded_string = "data:image;base64,"+base64.b64encode(image_file.read(-1)).decode('utf-8')
    
    return file_names

@register.simple_tag
def get_news_picture(user_uuid = "", news_uuid = "", file = ""):
    picture_path = news_pictures_path + '{}/{}/{}'.format(user_uuid, news_uuid, file)
    valid = False
    if os.path.isfile(picture_path) is False:
        with open(news_default_pic, "rb") as image_file:
            encoded_string = "data:image;base64,"+base64.b64encode(image_file.read(-1)).decode('utf-8')
    else:
        with open(picture_path, "rb") as image_file:
            encoded_string = "data:image;base64,"+base64.b64encode(image_file.read(-1)).decode('utf-8')
            valid = True
    return encoded_string, valid

def get_all_news_pictures(user_uuid = "", news_uuid = ""):
    news_path = news_pictures_path + '{}/{}'.format(user_uuid, news_uuid)
    pictures = []
    if os.path.isdir(document_path) is False:
        picture, valid = get_news_picture(user_uuid, news_uuid, filename)
        return pictures[picture]
    else:
        for filename in os.listdir(news_path):
            picture, valid = get_news_picture(user_uuid, news_uuid, filename)
            if(valid is False):
                return pictures[picture]
            else: pictures.append(picture)
        return pictures