from django.db import models
from Common.models import SoftDeletionModel
from safedelete.models import SafeDeleteModel
from safedelete.models import HARD_DELETE_NOCASCADE, SOFT_DELETE, NO_DELETE
from django.conf import settings
from Member.models import Physicians
# Rest_Framework
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers
# Create your models here.
from django.dispatch import receiver
import uuid
from django.db.models.signals import post_save



class DocCategories(models.Model):
    #_safedelete_policy = NO_DELETE
    name = models.CharField(max_length=50)
    rtl_name = models.CharField(max_length=50, default='منو', blank=True, null=True)
    index = models.IntegerField(default=0)
    # Integer field for icon uses icon names
    # which are integers to gets icon's paths
    icon = models.PositiveIntegerField(blank=True, null=True)
    icon_name = models.CharField(max_length=50, blank=True, null=True)

class DocCatSubmenu(models.Model):
    #_safedelete_policy = NO_DELETE
    name = models.CharField(max_length=50)
    index = models.IntegerField(default=0)
    rtl_name = models.CharField(max_length=50, default='ساب منو', blank=True, null=True)
    # Integer field for icon uses icon names
    # which are integers to gets icon's paths
    icon = models.PositiveIntegerField(blank=True, null=True)
    docCategories = models.ForeignKey(DocCategories, related_name='sub_menu', on_delete=models.PROTECT)

    '''def __str__(self):
        subMenuSerializer = DocCategoriesSubMenuSerializer(self)
        content = JSONRenderer().render(subMenuSerializer.data)
        #return '%s: %s' % (self.name, self.index)
        #return self[1]
        return str(content)'''

class Documents(models.Model):
    #_safedelete_policy = NO_DELETE
    title = models.CharField(max_length=100)
    date = models.DateField()
    SITES_CHOICES = (('Nikan','Nikan Hospital'), ('Mehrad', 'Mehrad Hospital'), ('Milad', 'Milad Hospital'))
    site = models.CharField(max_length = 30 ,choices = SITES_CHOICES, null = False)
    attachment = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=1000, blank=True, null=True)
    # Foreign Keys
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    category = models.ForeignKey(DocCategories, on_delete=models.PROTECT)
    doccatsubmenu = models.ForeignKey(DocCatSubmenu, on_delete=models.PROTECT)
    physician = models.ForeignKey(Physicians, on_delete=models.PROTECT)

@receiver(post_save, sender=Documents)
def create_document_UUID(sender, instance=None, created=False, **kwargs):
    if created:
        DocumentUUID.objects.create(document=instance, document_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id)))
class DocumentUUID(models.Model):
    document = models.OneToOneField(Documents, related_name='uuid_document', primary_key=True, on_delete=models.PROTECT)
    document_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

class HistoryCategory(models.Model):
    name = models.CharField(max_length=50)
    rtl_name = models.CharField(max_length=50, default='منو', blank=True, null=True)
    icon = models.PositiveIntegerField(blank=True, null=True)
    icon_name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    index = models.IntegerField(default=0, blank=True, null = True)

class PatientHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    context = models.CharField(max_length=100000)
    category = models.ForeignKey(HistoryCategory, on_delete=models.PROTECT, related_name='patient_histories')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user_created = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_created_history', on_delete=models.PROTECT)