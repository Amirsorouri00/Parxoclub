# Rest_Framework
from .models import DocCatSubmenu, DocCategories, Documents, HistoryCategory, \
    PatientHistory
from PatientDoc.models import HistoryCategory
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer


class DocCategoriesSubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocCatSubmenu
        fields = ('id', 'name', 'rtl_name', 'index', 'icon')

class DocCategoriesSerializer(serializers.ModelSerializer):
    #sub_menu = serializers.StringRelatedField(many=True, allow_null=True)
    sub_menu = DocCategoriesSubMenuSerializer(many=True)
    class Meta:
        model = DocCategories
        fields = ('id', 'name', 'rtl_name', 'index', 'icon', 'icon_name','sub_menu')

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
    uuid = serializers.CharField(source='uuid_document.document_uuid', read_only=True)
    class Meta:
        model = Documents
        fields = ('id', 'title', 'date', 'attachment', 'comment'
            , 'category_id', 'physician_id', 'user_id', 'doccatsubmenu_id', 'supervisor', 'prefix', 'uuid')

class HistoryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryCategory
        fields = ('id', 'name', 'rtl_name', 'icon', 'icon_name')

class PatientHistorySerializer(serializers.ModelSerializer):
    user_created_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_created_last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = PatientHistory
        fields = ('title', 'context', 'created_at', 'user_created_first_name', 'user_created_last_name')

class AllUsersHistorySerializer(serializers.ModelSerializer):
    patient_histories = PatientHistorySerializer(read_only=True)
    class Meta:
        model = HistoryCategory
        fields = ('name', 'rtl_name', 'icon', 'icon_name', 'index', 'patient_histories')

class GetUserHistorySerializer(serializers.ModelSerializer):
    user_created_first_name = serializers.CharField(source='user.first_name', read_only=True)   
    user_created_last_name = serializers.CharField(source='user.last_name', read_only=True)
    history_category_name = serializers.CharField(source='category.name', read_only=True)
    history_category_rtl_name = serializers.CharField(source='category.rtl_name', read_only=True)
    class Meta:
        model = PatientHistory
        fields = ('title', 'context', 'created_at', 'user_created_first_name', 'user_created_last_name', 'history_category_name', 'history_category_rtl_name')


class OneUserHistorySerializer(serializers.ModelSerializer):
    patient_histories = PatientHistorySerializer(read_only=True, many=True)
    class Meta:
        model = HistoryCategory
        fields = ('id', 'name', 'rtl_name', 'icon', 'icon_name', 'index', 'patient_histories')