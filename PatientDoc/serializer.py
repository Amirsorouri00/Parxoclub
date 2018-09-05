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
        fields = ('id', 'name', 'index', 'icon', 'icon_name','sub_menu')

class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ('id', 'title', 'date', 'attachment', 'comment'
            , 'category_id', 'physician_id', 'user_id', 'doccatsubmenu_id')

class SpecialistsHistoryObject(object):
    def __init__(self, prefixName, physicianFirstName, physicianLastName, title, num, *args):
        self.prefix_name = prefixName
        self.physician_first_name = physicianFirstName
        self.physician_last_name = physicianLastName
        self.title = title
        self.num = num
        # I have to add other Probable variable Here

class SpecialistsHistorySerializer(serializers.Serializer):
    prefix_name = serializers.CharField(max_length=50)
    physician_first_name = serializers.CharField(max_length=100)
    physician_last_name = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=50)
    num = serializers.IntegerField()

class MemberPanelDocumentsListSerializer(serializers.ModelSerializer):
    supervisor = serializers.CharField(source='physician.user.last_name', read_only=True)
    prefix = serializers.CharField(source='physician.prefix.name', read_only=True)
    class Meta:
        model = Documents
        fields = ('id', 'title', 'date', 'attachment', 'comment'
            , 'category_id', 'physician_id', 'user_id', 'doccatsubmenu_id', 'supervisor', 'prefix')