from django.shortcuts import render, redirect
from supplier.models import Supplier
from client.models import Client
from supplier.forms import SupplierForm
from client.forms import ClientForm


def main_page(request):
    return render(request, 'buy_together_app/main.html')


def description_page(request):
    return render(request, 'buy_together_app/description.html')


def signup_user(request, msg=""):
    form = SupplierForm()
    formm = ClientForm()
    context = {'form': form, 'formm': formm, 'message': [msg]}
    return render(request, 'buy_together_app/sign_up.html', context)


def signup_supplier(request):
    if request.method == 'POST':
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
        try:
            Supplier.save_supplier(supplier)
            return redirect('Main Page')
        except Exception:
            return signup_user(request, 'Username is taken')


def signup_client(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password_text = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        area = request.POST.get('area')
        client = Client(user_name=user_name,
                        password=password_text,
                        first_name=first_name,
                        last_name=last_name,
                        area=area)
        try:
            client.save_client()
            return redirect('Main Page')
        except Exception:
            return signup_user(request, 'Username is taken')
