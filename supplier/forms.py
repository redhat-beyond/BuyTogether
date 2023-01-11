from django import forms
from .models import Supplier
from django.contrib.auth.models import User


class SupplierForm(forms.Form):
    username = forms.CharField(label='username', min_length=6, max_length=32)
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='first_name', min_length=1)
    last_name = forms.CharField(label='last_name', min_length=1)
    business_name = forms.CharField(label='business_name', min_length=6, max_length=32)

    def save(self, commit=True):
        supplier = Supplier(
            supplier_account=User.objects.create_user(
                username=self.cleaned_data["username"],
                password=self.cleaned_data["password"],
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
            ),
            business_name=self.cleaned_data["business_name"],
        )
        Supplier.save_supplier(supplier)
        return supplier
