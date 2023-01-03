from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['user_name', 'password', 'first_name', 'last_name', 'business_name']
