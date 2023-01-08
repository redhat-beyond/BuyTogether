from .models import OrderedProduct
from client.models import Client
from supplier_product.models import SupplierProduct
from delivery_location.models import DeliveryLocation
from product.models import Product
from supplier.models import Supplier
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError


def client_check(user):
    try:
        return Client.objects.get(client_account=user)
    except ObjectDoesNotExist:
        return False


@user_passes_test(client_check, login_url='Main Page')
def change_quantity(request, order_id):
    try:
        quantity = int(request.GET['quantity'])
    except MultiValueDictKeyError:
        return redirect('/client/')
    except ValueError:
        return redirect('/client/')
    try:
        ordered_product = OrderedProduct.objects.get(id=int(order_id))
    except ObjectDoesNotExist:
        return redirect('/client/')
    if (quantity > 0):
        ordered_product.increase_quantity(quantity)
    elif (quantity < 0):
        ordered_product.decrease_quantity(abs(quantity))
    return redirect('/client/')


@user_passes_test(client_check, login_url='Main Page')
def delete_order(request, order_id):
    try:
        OrderedProduct.objects.get(id=int(order_id)).delete_ordered_product()
    except ObjectDoesNotExist:
        return redirect('Main Page')
    return redirect('/client/')


@user_passes_test(client_check, login_url='Main Page')
def order(request):
    return render(request, 'ordered_product/new_order.html', {})


@user_passes_test(client_check, login_url='Main Page')
def get_products_by_product_name(request):
    prod_name = str(request.GET['product_name'])
    message = ""
    supplier_products = []
    try:
        product = Product.objects.get(product_name=prod_name)
        supplier_products = SupplierProduct.objects.filter(qr_code=product)
    except ObjectDoesNotExist:
        message = "Invalid product name"
    if not supplier_products and message != "Invalid product name":
        message = "No products found"
    return render(
        request,
        'ordered_product/new_order.html',
        {'supplier_products': supplier_products, 'message': message}
    )


@user_passes_test(client_check, login_url='Main Page')
def get_products_by_client_area(request):
    message = ""
    client = client_check(request.user)
    supplier_products = []
    deliveries_in_client_area = DeliveryLocation.objects.filter(location=client.area)
    if not deliveries_in_client_area:
        message = "No products found in your area"
    else:
        for delivery in deliveries_in_client_area:
            supplier_products += list(SupplierProduct.objects.filter(user_name=delivery.user_name))
        if supplier_products == []:
            message = "No products found"
    return render(
        request,
        'ordered_product/new_order.html',
        {'supplier_products': supplier_products, 'message': message}
    )


@user_passes_test(client_check, login_url='Main Page')
def get_products_by_supplier_user_name(request):
    supplier_user_name = str(request.GET['supplier_user_name'])
    message = ""
    supplier_products = []
    try:
        user = User.objects.get(username=supplier_user_name)
        supplier = Supplier.objects.get(supplier_account=user)
    except ObjectDoesNotExist:
        message = "Supplier no found"

    if message != "Supplier no found":
        client = client_check(request.user)
        deliveries = DeliveryLocation.filter_by_supplier_and_location(supplier, client.area)
        if not deliveries:
            message = "No products found in your area"
        else:
            supplier_products = SupplierProduct.objects.filter(user_name=supplier)
            if not supplier_products:
                message = "No products found"
    return render(
        request,
        'ordered_product/new_order.html',
        {'supplier_products': supplier_products, 'message': message}
    )


@user_passes_test(client_check, login_url='Main Page')
def find_delivery(request, supplier_product_id):
    try:
        supplier_product = SupplierProduct.objects.get(supplier_product_id=int(supplier_product_id))
    except ObjectDoesNotExist:
        return redirect('/client/')
    client = client_check(request.user)
    deliveries = DeliveryLocation.filter_by_supplier_and_location(supplier_product.user_name, client.area)
    message = ""
    if not deliveries:
        message = "No delivery found at '"+client.area+"'"
    return render(
        request,
        'ordered_product/new_order.html',
        {'deliveries': deliveries, 'sup_pro_id': supplier_product_id, 'message': message}
    )


@user_passes_test(client_check, login_url='Main Page')
def order_summary(request, supplier_product_id, delivery_location_id):
    try:
        supplier_product = SupplierProduct.objects.get(supplier_product_id=int(supplier_product_id))
        delivery_location = DeliveryLocation.objects.get(id=int(delivery_location_id))
    except ObjectDoesNotExist:
        return redirect('/client/')
    return render(
        request,
        'ordered_product/new_order.html',
        {'delivery_location': delivery_location, 'supplier_product': supplier_product}
    )


@user_passes_test(client_check, login_url='Main Page')
def complete_order(request, supplier_product_id, delivery_location_id):
    try:
        quantity = int(request.GET['quantity'])
    except MultiValueDictKeyError:
        return redirect('/client/')
    except ValueError:
        return redirect('/client/')
    try:
        delivery_location = DeliveryLocation.objects.get(id=int(delivery_location_id))
        supplier_product = SupplierProduct.objects.get(supplier_product_id=int(supplier_product_id))
    except ObjectDoesNotExist:
        return redirect('/client/')

    OrderedProduct.order(delivery_location, client_check(request.user), supplier_product, quantity)
    return redirect('/client/')


@user_passes_test(client_check, login_url='Main Page')
def pay_order(request):
    return render(request, 'ordered_product/pay_order.html', {})
