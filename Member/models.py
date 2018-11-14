from Common.models import SoftDeletionModel
from safedelete.models import SafeDeleteModel
from safedelete.models import HARD_DELETE_NOCASCADE, SOFT_DELETE, NO_DELETE
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import pre_delete 
from django.dispatch import receiver
import uuid
#from django_mysql.models import JSONField, Model

# rest_framework Post-Save token generator
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_UUID(sender, instance=None, created=False, **kwargs):
    if created:
        UserUUID.objects.create(user=instance, user_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id)))

class UserUUID(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='uuid_user', primary_key=True, on_delete=models.PROTECT)
    user_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

class Profile(models.Model):
    #_safedelete_policy = NO_DELETE
    # Foreign Keys
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile_user', primary_key=True, on_delete=models.PROTECT)
    # Columns
    code = models.CharField(max_length=20, db_index=True, unique=True)
    rtl_first_name = models.CharField(max_length=50, default='تست',  blank=True, null=True)
    rtl_last_name = models.CharField(max_length=50, default='تست', blank=True, null=True)
    pkey = models.CharField(max_length=100, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    GENDER_CHOICES = (('M','Male'), ('F', 'Female'))
    maleOrFemale = models.CharField(max_length = 8 ,choices = GENDER_CHOICES, null = False)
    gender = models.BooleanField(default=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    photo = JSONField(blank=True, null=True)

class Memberships(models.Model):
    #_safedelete_policy = NO_DELETE
    name = models.CharField(max_length=50)
    rtl_name = models.CharField(max_length=50, default='طلایی', blank=True, null=True)
    index = models.IntegerField(default=0)
    #done

class Prefixes(models.Model):
    #_safedelete_policy = NO_DELETE
    name = models.CharField(max_length=50, blank=True, null=True)
    rtl_name = models.CharField(max_length=50, default='دکتر', blank=True, null=True)

class Expertises(models.Model):
    #_safedelete_policy = NO_DELETE
    name = models.CharField(max_length=50, blank=True, null=True)
    rtl_name = models.CharField(max_length=50, default='قلب', blank=True, null=True)

class Physicians(models.Model):
    #_safedelete_policy = NO_DELETE
    # Foreign Keys
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='physician_user', primary_key=True, on_delete=models.PROTECT)
    prefix = models.ForeignKey(Prefixes, related_name='physician_prefix', on_delete=models.PROTECT)
    expertise = models.ForeignKey(Expertises, related_name='physician_expertise',on_delete=models.PROTECT, blank=True, null=True)

class Members(models.Model):
    #_safedelete_policy = NO_DELETE
    code = models.CharField(max_length=20, db_index=True, unique=True, blank=True, null=True)
    # Foreign Keys
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='member_user', primary_key=True, on_delete=models.PROTECT)
    membership = models.ForeignKey(Memberships, related_name='member_membership', on_delete=models.PROTECT)
    physician = models.ForeignKey(Physicians, related_name='member_physician', blank=True, null=True, on_delete=models.PROTECT)
    profile = models.ForeignKey(Profile, related_name='member_profile', on_delete=models.PROTECT)
    #prefix = models.ForeignKey(Prefixes, related_name='member_prefix', on_delete=models.PROTECT, blank=True, null = True)

class Group_Have_Perm(models.Model):
    #_safedelete_policy = NO_DELETE
    name = models.CharField(max_length=50)
    index = models.IntegerField(default=0)
    # Foreign Keys
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

class Group_Give_Perm(models.Model):
    #_safedelete_policy = NO_DELETE
    name = models.CharField(max_length=50)
    index = models.IntegerField(default=0)
    # Foreign Keys
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

class UserGroup(models.Model):
    #_safedelete_policy = NO_DELETE
    class Meta:
        unique_together = (('user_id', 'haveOrGive'))
    # Foreign Keys
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    HAVE = 'have'
    GIVE = 'give'
    GROUP_CHOICES = ((HAVE,'have'), (GIVE, 'give'))
    haveOrGive = models.CharField(max_length = 5 ,choices = GROUP_CHOICES, null = False)
    groupH = models.ForeignKey(Group_Have_Perm, on_delete=models.PROTECT)
    groupG = models.ForeignKey(Group_Give_Perm, on_delete=models.PROTECT)
    def is_have(self):
        return self.GROUP_CHOICES in (self.HAVE, self.GIVE)
