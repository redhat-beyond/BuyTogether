from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['user_name', 'password', 'first_name', 'last_name', 'area']
