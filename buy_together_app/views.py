from django.shortcuts import render


def main_page(request):
    return render(request, 'buy_together_app/main.html')
