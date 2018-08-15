from django import forms
from django.forms import ModelForm, ModelChoiceField
# Models
from .models import Memberships, Members, Physicians, Profile
from django.db.models.functions import Concat
from django.contrib.auth.models import User

# Common
from Common.constants import CHOICES

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "First Name"
        self.fields['first_name'].widget = forms.TextInput(attrs={
            'id': 'maintenance_first_name_id',
            'class': 'maintenance_first_name_class',
            'name': 'first_name',
            'placeholder': 'amirso'})
        self.fields['last_name'].label = "Last Name"
        self.fields['last_name'].widget = forms.TextInput(attrs={
            'id': 'maintenance_last_name_id',
            'class': 'maintenance_last_name_class',
            'name': 'last_name',
            'placeholder': 'amirso'})
        self.fields['email'].label = "Email"
        self.fields['email'].widget = forms.EmailInput(attrs={
            'id': 'maintenance_email_id',
            'class': 'maintenance_email_class',
            'name': 'email',
            'placeholder': 'amirso'})

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['birthdate', 'mobile', 'address', 'gender']
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['birthdate'].label = "Birth Date"
        self.fields['birthdate'].widget = forms.TextInput(attrs={
            'id': 'maintenance_birthdate_id',
            'class': 'maintenance_birthdate_class',
            'name': 'birthdate',
            'placeholder': 'amirso'})
        self.fields['mobile'].label = "Phone"
        self.fields['mobile'].widget = forms.TextInput(attrs={
            'id': 'maintenance_mobile_id',
            'class': 'maintenance_mobile_class',
            'name': 'mobile',
            'placeholder': 'amirso'})
        self.fields['address'].label = "Address"
        self.fields['address'].widget = forms.TextInput(attrs={
            'id': 'maintenance_address_id',
            'class': 'maintenance_address_class',
            'name': 'address',
            'placeholder': 'amirso'})
        self.fields['gender'].label = "Gender"
        self.fields['gender'].widget = forms.CheckboxInput(attrs={
            'id': 'maintenance_gender_id',
            'class': 'maintenance_gender_class',
            'name': 'gender',
            'placeholder': 'amirso'})

class MemberForm(ModelForm):
    class Meta:
        model = Members
        fields = ['code', 'membership']
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['code'].label = "Membership ID"
        self.fields['code'].widget = forms.TextInput(attrs={
            'id': 'maintenance_member_code_id',
            'class': 'maintenance_member_code_class',
            'name': 'member_code',
            'placeholder': 'amirso'})
        self.fields['membership'].label = "Membership Type"
        self.fields['membership'].widget = forms.Select(attrs={
            'id': 'maintenance_membership_type_id',
            'class': 'maintenance_membership_type_class',
            'name': 'membership_type',
            'placeholder': 'amirso'},choices = CHOICES)

# class MembershipForm(ModelForm):
#     class Meta:
#         model = Memberships
#         fields = ['name']
#     def __init__(self, *args, **kwargs):
#         super(MembershipForm, self).__init__(*args, **kwargs)
#         self.fields['name'].label = "Membership Type"
#         self.fields['name'].widget = forms.Select(attrs={
#             'id': 'maintenance_membership_type_id',
#             'class': 'maintenance_membership_type_class',
#             'name': 'membership_type',
#             'placeholder': 'amirso'},choices = CHOICES)