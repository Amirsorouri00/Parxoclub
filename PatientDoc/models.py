from django.db import models
from django.conf import settings
from Member.models import Physicians
# Create your models here.

class DocCategories(models.Model):
    name = models.CharField(max_length=50)
    index = models.IntegerField(default=0)
    # Integer field for icon uses icon names
    # which are integers to gets icon's paths
    icon = models.PositiveIntegerField(blank=True, null=True)

class Documents(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    attachment = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=1000, blank=True, null=True)
    # Foreign Keys
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    category = models.ForeignKey(DocCategories, on_delete=models.PROTECT)
    physician = models.ForeignKey(Physicians, on_delete=models.PROTECT)