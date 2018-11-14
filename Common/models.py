from django.db import models
from django.utils import timezone
from django.conf import settings
from safedelete.models import SafeDeleteModel
from safedelete.models import HARD_DELETE_NOCASCADE, SOFT_DELETE, NO_DELETE
# Create your models here.

class SoftDeletionQuerySet(models.QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)

class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()


from Member.models import Group_Have_Perm as GH, Group_Give_Perm as GG
class Page(models.Model):
    #_safedelete_policy = SOFT_DELETE
    class Meta:
        unique_together = (('id', 'name'))
    pageId = models.DecimalField(decimal_places=3, max_digits=3)
    name = models.CharField(max_length = 20)

class Object(models.Model):
    #_safedelete_policy = SOFT_DELETE
    class Meta:
        unique_together = (('className', 'page_id'))
    objectId = models.DecimalField(decimal_places=3, max_digits=3)
    className = models.CharField(max_length = 40)
    idName = models.CharField(max_length = 40)
    # Foreign Key
    page_id = models.ForeignKey(Page, on_delete=models.PROTECT)

class Group_For_Objects(models.Model):
    #_safedelete_policy = SOFT_DELETE
    #just Have Id
    comment = models.CharField(max_length = 20, null = False, blank = False)

class ObjectGroup(models.Model):
    #_safedelete_policy = SOFT_DELETE
    class Meta:
        unique_together = (('pageObject_id', 'group_id'))
    # Foreign Key
    pageObject_id = models.ForeignKey(Object, on_delete=models.PROTECT)
    group_id = models.ForeignKey(Group_For_Objects, on_delete=models.PROTECT)

class GroupPermission(models.Model):
    #_safedelete_policy = SOFT_DELETE
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
    #_safedelete_policy = SOFT_DELETE
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
    #_safedelete_policy = SOFT_DELETE
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
