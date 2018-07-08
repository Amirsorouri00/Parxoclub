from django.db import models
from django.conf import settings
#from django_mysql.models import JSONField, Model

# Create your models here.

class Profile(models.Model):
    # Foreign Keys
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.PROTECT)
    # Columns
    pkey = models.CharField(max_length=100, blank=False, null=False)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.BooleanField(default=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    #photo = JSONField(blank=True)

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

class Group(models.Model):
    name = models.CharField(max_length=50)
    index = models.IntegerField(default=0)
    # Foreign Keys
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

class UserGroup(models.Model):
    # Foreign Keys
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.PROTECT)
    Group = models.ForeignKey(Group, on_delete=models.PROTECT)