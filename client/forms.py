from django import forms
from django.contrib.auth.models import User
from .models import Client


class ClientForm(forms.Form):
    username = forms.CharField(label='useasdrname', min_length=6, max_length=32)
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='first_name', min_length=1)
    last_name = forms.CharField(label='last_name', min_length=1)
    area = forms.CharField(label='area', min_length=1, max_length=32)

    def save(self, commit=True):
        client = Client(
            client_account=User.objects.create_user(
                username=self.cleaned_data["username"],
                password=self.cleaned_data["password"],
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
            ),
            area=self.cleaned_data["area"],
        )

        client.save_client()
        return client
