from collections import namedtuple
# Rest_Framework
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers
# Models
from .models import Members, Profile, Memberships, Prefixes, Physicians, Expertises
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import datetime
from datetime import timedelta
import time
from django.core.files import File
import os
import uuid
Maintenance_users = namedtuple('Users', ('user', 'member', 'physician'))

# class MaintenanceUsersSerializer(viewsets.ViewSet):
#     def list(self, request):
#         users = Maintenance_users(
#             user = Users.objects.all(),
#             member = Members.objects.all(),
#             Physicians
#         )


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memberships
        fields = ('name')

class MemberSerializer(serializers.ModelSerializer):
    #membership_set = MembershipSerializer(read_only=True, many=True)
    membership_set = serializers.CharField(source='membership.name', read_only=True)
    class Meta:
        model = Members
        depth = 1
        fields = ('code', 'user_id', 'membership_set')
        # , 'member_physician', 'member_user', 'member_profile'

class PhysicianSerializer(serializers.ModelSerializer):
    # physician_prefix = PrefixSerializer(many=True)
    # physician_expertise = ExpertiseSerializer(many=True)
    class Meta:
        model = Physicians
        fields = "('physician_prefix', 'physician_expertise')"

class PrefixSerializer(serializers.ModelSerializer): 
    physician_user = PhysicianSerializer()   
    class Meta:
        model = Prefixes
        fields = ('name', 'physician_prefix')

class ExpertiseSerializer(serializers.ModelSerializer):
    physician_expertise = PhysicianSerializer()
    class Meta:
        model = Expertises
        fields = ('name', 'physician_expertise')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'password', 'last_login', 'is_superuser', 'username', 'first_name'
            , 'last_name', 'email', 'is_staff', 'is_active', 'date_joined')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('birthdate', 'gender', 'mobile', 'address', 'photo')

class MaintenanceUsersSerializer(serializers.ModelSerializer):
    #physician_user = PhysicianSerializer()
    member_user = MemberSerializer()
    profile_user = ProfileSerializer()
    membership_set = serializers.CharField(source='user.member.membership_set.name', read_only=True)
    uuid = serializers.CharField(source='uuid_user.user_uuid.hex', read_only=True)
    #physician_prefix = PrefixSerializer()
    #member = Members.objects.get(user_id = self.get_current_user).select_related('membership')
    #membership = member.memberships.name
    class Meta:
        model = User
        fields = ('uuid', 'first_name', 'last_name', 'email', 'membership_set','member_user','profile_user')

class TokenSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    class Meta:
        model = Token
        fields = ('key', 'created', 'first_name')

class MemberSearchSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    #member_user = MemberSerializer()
    member_profile = ProfileSerializer(read_only=True)
    membership_set = serializers.CharField(source='membership.name', read_only=True)
    expertise = serializers.CharField(source='physician.expertise.name', read_only=True)
    prefix = serializers.CharField(source='physician.prefix.name', read_only=True)
    email = serializers.CharField(source='profile.email', read_only=True)
    mobile = serializers.CharField(source='profile.mobile', read_only=True)
    birthdate = serializers.DateField(source='profile.birthdate', read_only=True)
    address = serializers.CharField(source='profile.address', read_only=True)
    uuid = serializers.CharField(source='user.uuid_user.user_uuid.hex', read_only=True)
    # Check
    #age = datetime.utcnow() - time.strptime(str(birthdate), "%y-%m-%d")  
    #age = datetime.datetime.now() - time.strptime(str(birthdate), "%Y-%m-%d")
    class Meta:
        model = Members
        fields = ('uuid', 'user', 'membership_set','member_profile', 'expertise', 'prefix', 'email', 'birthdate', 'mobile', 'address')
