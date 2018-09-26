from django import forms
from django.forms import ModelForm, ModelChoiceField
from Member.models import Physicians
from .models import Documents

class PhysicianModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}. {} {}".format(obj.prefix.name, obj.user.first_name, obj.user.last_name)

class DocumentForm(ModelForm):
    physician = PhysicianModelChoiceField(Physicians.objects.all(), empty_label=None)
    
    class Meta:
        model = Documents
        fields = ['title', 'date', 'comment', 'physician']