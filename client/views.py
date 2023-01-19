from .models import Client
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from ordered_product.models import OrderedProduct


def client_check(user):
    try:
        return Client.objects.get(client_account=user)
    except Exception:
        return False


@user_passes_test(client_check, login_url='Main Page')
def clients_page(request):
    message = ""
    ordered_products = OrderedProduct.filter_user_name(client_check(request.user))
    if not ordered_products:
        message = "No orders found"
    sum_of_all_orders = sum(order_product.total_price() for order_product in ordered_products)
    return render(request, 'client/clients.html', {'orders': ordered_products,
                                                   'message': message,
                                                   'sum': sum_of_all_orders})
