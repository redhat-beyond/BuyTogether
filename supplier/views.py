from django.shortcuts import render, redirect
from supplier.models import Supplier
from .forms import SupplierForm


def signup_supplier(request):
    form = SupplierForm()
    context = {'form': form, 'message': ['username should be longer than 6',
                                         'password should be longer than 6',
                                         'business name should be longer than 6']}
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        user_name = request.POST.get('user_name')
        password_text = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        business_name = request.POST.get('business_name')
        supplier = Supplier(user_name=user_name,
                            password=password_text,
                            first_name=first_name,
                            last_name=last_name,
                            business_name=business_name)
        if form.is_valid():
            Supplier.save_supplier(supplier)
            return redirect('Main Page')
        else:
            try:
                Supplier.save_supplier(supplier)
            except Exception:
                context['message'].append('User name is taken')
                return render(request, 'supplier/supplier_sign_up.html', context)
    return render(request, 'supplier/supplier_sign_up.html', context)
