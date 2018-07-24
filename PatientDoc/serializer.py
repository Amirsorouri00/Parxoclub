# Rest_Framework
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers
# Models
from .models import DocCategories, DocCatSubmenu, Documents

class DocCategoriesSubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocCatSubmenu
        fields = ('id', 'name', 'index', 'icon')

class DocCategoriesSerializer(serializers.ModelSerializer):
    #sub_menu = serializers.StringRelatedField(many=True, allow_null=True)
    sub_menu = DocCategoriesSubMenuSerializer(many=True)
    class Meta:
        model = DocCategories
        fields = ('id', 'name', 'index', 'icon', 'sub_menu')

class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ('id', 'title', 'date', 'attachment', 'comment'
            , 'category_id', 'physician_id', 'user_id', 'doccatsubmenu_id')
