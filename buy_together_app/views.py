from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


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
