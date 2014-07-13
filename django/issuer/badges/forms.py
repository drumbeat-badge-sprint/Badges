'''
Created on Apr 16, 2011

@author: Mike_Edwards
'''
from django.forms.models import ModelChoiceField, ModelForm
from django.forms.widgets import HiddenInput
from badges.models import BadgeRequest, Badge, Issuer

class BadgeRequestForm(ModelForm):
    badge = ModelChoiceField(Badge.objects.all(),widget=HiddenInput)
    issuer = ModelChoiceField(Issuer.objects.all(),widget=HiddenInput)
    
    class Meta:
        model = BadgeRequest
        exclude = ['expires','user',]