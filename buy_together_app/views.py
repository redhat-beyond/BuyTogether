from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from client.forms import ClientForm
from supplier.forms import SupplierForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


def main_page(request):
    return render(request, 'buy_together_app/main.html')


def description_page(request):
    return render(request, 'buy_together_app/description.html')


def log_in_page(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        user_pass = request.POST.get('password')
        user = authenticate(request, username=user_name, password=user_pass)
        if user is not None:
            login(request, user)
            return redirect('Main Page')
        else:
            messages.info(request, 'User name OR Password is incorrect')
    return render(request, 'buy_together_app/login.html')


def not_allowed_page(request):
    return render(request, 'buy_together_app/not_allowed.html')


def signup_user(request, msg="", invalid={}):
    supplier_form = SupplierForm()
    client_form = ClientForm()
    context = {'supplier_form': supplier_form, 'client_form': client_form, 'message': [msg], 'invalid': invalid}
    return render(request, 'buy_together_app/sign_up.html', context)


def signup_supplier(request):
    return signup(request, SupplierForm)


def signup_client(request):
    return signup(request, ClientForm)


def signup(request, form_type):
    if request.method == 'POST':
        form = form_type(request.POST)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                return signup_user(request, 'Username is taken')
            return redirect('Main Page')
        return signup_user(request, msg="Request is invalid", invalid=form.errors.as_json())
    else:
        return signup_user(request, 'Please sign up')


@login_required
def logout_user(request):
    logout(request)
    return redirect('Main Page')
