from django.db import models
from Member.models import Group
from src.django.tests import max_lengths
from django.utils import timezone
from django.conf import settings
# Create your models here.
'''
class Pages(models.Model):
    name = models.CharField(max_lengths = 20)
    .
    .
    .

class Objects(models.Model):
    name = models.CharField(max_lengths = 20)
    .
    .
    .
'''
class GroupPermission(models.Model):
    '''class Meta:
        unique_together = (('group', 'page_id', 'object_id'))'''
    id = models.PositiveIntegerField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    page_id = models.IntegerField()
    object_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    last_modified = models.DateTimeField(db_index=True, auto_now=True)
    # Foreign Key
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

class GroupHavePermission(models.Model):
    '''class Meta:
        unique_together = (('group', 'page_id', 'object_id'))'''
    id = models.PositiveIntegerField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    page_id = models.IntegerField()
    object_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    last_modified = models.DateTimeField(db_index=True, auto_now=True)
    # Foreign Key
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

class GroupDoesntHavePermission(models.Model):
    '''class Meta:
        unique_together = (('group', 'page_id', 'object_id'))'''
    id = models.PositiveIntegerField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    page_id = models.IntegerField()
    object_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    last_modified = models.DateTimeField(db_index=True, auto_now=True)
    # Foreign Key
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)