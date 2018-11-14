import os, glob, base64
from django import template
from django.conf import settings

user_pictures_path = settings.PIC_UPLOAD_URL
user_default_pic = settings.PIC_UPLOAD_URL + 'default'
register = template.Library()

@register.simple_tag
def profile_pic(file_name="", cropped=True):
    file_suffix = "_cropped" if cropped else ""
    file_path = "/static/uploads/profilePics/{}{}".format(file_name, file_suffix)
    
    if os.path.isfile("./common" + file_path) is False:
        file_path = "/static/uploads/profilePics/default"

    with open("./common" + file_path, "rb") as image_file:
        encoded_string = "data:image;base64,"+base64.b64encode(image_file.read(-1)).decode('utf-8')
    
    return encoded_string

@register.simple_tag
def amir_profile_pic(user_uuid="", cropped=True):
    file_suffix = "_cropped" if cropped else ""
    file_path = "static/uploads/profilePics/{}/{}".format(user_uuid, 'amir.png')
    file_path = '{}/{}'.format(user_uuid, 'amir.png')
    if os.path.isfile(settings.PIC_UPLOAD_URL +  file_path) is False:
        file_path = "static/uploads/profilePics/default"
        with open('/var/www/praxo-co.ir/' +  file_path, "rb") as image_file:
            encoded_string = "data:image;base64,"+base64.b64encode(image_file.read(-1)).decode('utf-8')
    else:
        with open(settings.PIC_UPLOAD_URL +  file_path, "rb") as image_file:
            encoded_string = "data:image;base64,"+base64.b64encode(image_file.read(-1)).decode('utf-8')
    return encoded_string

def get_user_picture(user_uuid = ""):
    picture_path = user_pictures_path + '{}'.format(user_uuid)
    valid = False
    if os.path.isdir(picture_path) is False:
        with open(user_default_pic, "rb") as image_file:
            encoded_string = "data:image;base64,"+base64.b64encode(image_file.read(-1)).decode('utf-8')
    else:
        for filename in os.listdir(picture_path):
            with open(picture_path + '/' + filename, "rb") as image_file:
                encoded_string = "data:image;base64,"+base64.b64encode(image_file.read(-1)).decode('utf-8')
                valid = True
    return encoded_string, valid