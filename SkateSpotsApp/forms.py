from django import forms
from .models import *


class MarkerForm(forms.ModelForm):

    class Meta:
        model = Marker
        fields = ['name', 'photo','desc', 'lat', 'long', 'kind']


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'password', 'birthday', 'photo']
