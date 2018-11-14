import os, glob, base64
from django import template
from django.conf import settings

register = template.Library()

document_pictures_path = settings.DOC_UPLOAD_URL
document_default_pic = settings.STATIC_ROOT + 'img/fileNotFound.svg'

@register.simple_tag
def document_pic_name(user_uuid = "", doc_uuid = ""):
    document_path = document_pictures_path + '{}/{}'.format(user_uuid, doc_uuid)
    file_names = []
    if os.path.isdir(document_path) is False:
        info = os.stat(document_default_pic)
        data = {'name': 'filename', 'size': info.st_size}
        file_names.append(data)
    else:
        for filename in os.listdir(document_path):
            info = os.stat(document_path + '/' + filename)
            print(info.st_mtime)
            print(info.st_size)
            data = {'name': filename, 'size': info.st_size}
            file_names.append(data)
    # with open("./common" + file_path, "rb") as image_file:
    #     encoded_string = "data:image;base64,"+base64.b64encode(image_file.read(-1)).decode('utf-8')
    
    return file_names

@register.simple_tag
def get_document_picture(user_uuid = "", doc_uuid = "", file = ""):
    picture_path = document_pictures_path + '{}/{}/{}'.format(user_uuid, doc_uuid, file)
    valid = False
    if file == "":
        encoded_string = "in get_document_picture and file is empty"
        return encoded_string, False
    if os.path.isfile(picture_path) is False:
        with open(document_default_pic, "rb") as image_file:
            encoded_string = "data:image;base64,"+base64.b64encode(image_file.read(-1)).decode('utf-8')
    else:
        with open(picture_path, "rb") as image_file:
            encoded_string = "data:image;base64,"+base64.b64encode(image_file.read(-1)).decode('utf-8')
            valid = True
    #return valid, valid
    return encoded_string, valid

def get_all_document_pictures(user_uuid = "", doc_uuid = ""):
    document_path = document_pictures_path + '{}/{}'.format(user_uuid, doc_uuid)
    pictures = []
    if os.path.isdir(document_path) is False:
        picture, valid = get_document_picture(user_uuid, doc_uuid, '')
        info = os.stat(document_default_pic)
        data = {'name': 'fileNotFound.svg', 'size': info.st_size, 'picture': picture}
        pictures.append(data)
        #pictures.append('in get_all_document_pictures it is invalid path')
        return pictures
        
    else:
        filename = ''
        for filename in os.listdir(document_path):
            picture, valid = get_document_picture(user_uuid, doc_uuid, filename)
            info = os.stat(document_path + '/' + filename)
            if(valid is False):
                data = {'name': filename, 'size': info.st_size, 'picture': picture}
                pictures.append(data)
                return pictures
            else: 
                data = {'name': filename, 'size': info.st_size, 'picture': picture}
                pictures.append(data) 
        return pictures