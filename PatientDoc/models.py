from django.db import models
from django.conf import settings
from Member.models import Physicians
# Rest_Framework
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers
# Create your models here.

class DocCategories(models.Model):
    name = models.CharField(max_length=50)
    index = models.IntegerField(default=0)
    # Integer field for icon uses icon names
    # which are integers to gets icon's paths
    icon = models.PositiveIntegerField(blank=True, null=True)

class DocCatSubmenu(models.Model):
    name = models.CharField(max_length=50)
    index = models.IntegerField(default=0)
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
    title = models.CharField(max_length=100)
    date = models.DateField()
    attachment = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=1000, blank=True, null=True)
    # Foreign Keys
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    category = models.ForeignKey(DocCategories, on_delete=models.PROTECT)
    doccatsubmenu = models.ForeignKey(DocCatSubmenu, on_delete=models.PROTECT)
    physician = models.ForeignKey(Physicians, on_delete=models.PROTECT)