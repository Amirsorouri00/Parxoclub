from django.db import models
from Member.models import Group_Have_Perm as GH, Group_Give_Perm as GG
from django.utils import timezone
from django.conf import settings
# Create your models here.

class Page(models.Model):
    class Meta:
        unique_together = (('id', 'name'))
    pageId = models.DecimalField(decimal_places=3, max_digits=3)
    name = models.CharField(max_length = 20)

class Object(models.Model):
    class Meta:
        unique_together = (('className', 'page_id'))
    objectId = models.DecimalField(decimal_places=3, max_digits=3)
    className = models.CharField(max_length = 40)
    idName = models.CharField(max_length = 40)
    # Foreign Key
    page_id = models.ForeignKey(Page, on_delete=models.PROTECT)

class Group_For_Objects(models.Model):
    #just Have Id
    comment = models.CharField(max_length = 20, null = False, blank = False)

class ObjectGroup(models.Model):
    class Meta:
        unique_together = (('pageObject_id', 'group_id'))
    # Foreign Key
    pageObject_id = models.ForeignKey(Object, on_delete=models.PROTECT)
    group_id = models.ForeignKey(Group_For_Objects, on_delete=models.PROTECT)

class GroupPermission(models.Model):
    class Meta:
        unique_together = (('page_id', 'object_id'))
    page_id = models.IntegerField()
    object_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    last_modified = models.DateTimeField(db_index=True, auto_now=True)
    # Foreign Key
    groupHavePerm = models.ForeignKey(GH, on_delete=models.PROTECT)
    groupGivePerm = models.ForeignKey(GG, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

class GroupHavePermission(models.Model):
    class Meta:
        unique_together = (('page_id', 'object_id'))
    page_id = models.IntegerField()
    object_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    last_modified = models.DateTimeField(db_index=True, auto_now=True)
    # Foreign Key
    groupHavePerm = models.ForeignKey(GH, on_delete=models.PROTECT)
    groupGivePerm = models.ForeignKey(GG, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

class GroupDoesntHavePermission(models.Model):
    class Meta:
        unique_together = (('page_id', 'object_id'))
    page_id = models.IntegerField()
    object_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    last_modified = models.DateTimeField(db_index=True, auto_now=True)
    # Foreign Key
    groupHavePerm = models.ForeignKey(GH, on_delete=models.PROTECT)
    groupGivePerm = models.ForeignKey(GG, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    