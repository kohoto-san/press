from blog.models import SubscribeEmail
from django.forms import ModelForm

from django import forms


class SubscribeEmailForm(ModelForm):

    class Meta:
        model = SubscribeEmail
        fields = ['email']
