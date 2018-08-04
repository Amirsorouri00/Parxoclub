from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
#from django.contrib.postgres.fields import JSONField
from django_mysql.models import JSONField, Model

# rest_framework Post-Save token generator
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Profile(models.Model):
    # Foreign Keys
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.PROTECT)
    # Columns
    pkey = models.CharField(max_length=100, blank=False, null=False)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.BooleanField(default=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    photo = JSONField(blank=True)

class Memberships(models.Model):
    name = models.CharField(max_length=50)
    index = models.IntegerField(default=0)
    #done

class Members(models.Model):
    code = models.CharField(max_length=20, db_index=True, unique=True)
    # Foreign Keys
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.PROTECT)
    membership = models.ForeignKey(Memberships, on_delete=models.PROTECT)

class Prefixes(models.Model):
    name = models.CharField(max_length=50)

class Physicians(models.Model):
    # Foreign Keys
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.PROTECT)
    prefix = models.ForeignKey(Prefixes, on_delete=models.PROTECT)

class Group_Have_Perm(models.Model):
    name = models.CharField(max_length=50)
    index = models.IntegerField(default=0)
    # Foreign Keys
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

class Group_Give_Perm(models.Model):
    name = models.CharField(max_length=50)
    index = models.IntegerField(default=0)
    # Foreign Keys
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

class UserGroup(models.Model):
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
