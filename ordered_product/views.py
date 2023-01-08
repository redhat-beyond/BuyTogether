from django.shortcuts import render
from .models import OrderedProduct
from client.models import Client
from supplier.models import Supplier
from supplier_product.models import SupplierProduct
from delivery_location.models import DeliveryLocation
from django.shortcuts import redirect


def order_list(request):
    if isinstance(request.user, Supplier):
        return redirect('Main Page')
    ordered_products = OrderedProduct.filter_user_name(Client(request.user))
    return render(request, 'ordered_product/orders.html', {'orders': ordered_products})


def change_quantity(request, order_id):
    quantity = request.GET['quantity']
    if (int(quantity) > 0):
        OrderedProduct.objects.get(id=int(order_id)).increase_quantity(int(quantity))
    elif (int(quantity) < 0):
        OrderedProduct.objects.get(id=int(order_id)).decrease_quantity(abs(int(quantity)))
    return redirect('orders')


def delete_order(request, order_id):
    OrderedProduct.objects.get(id=int(order_id)).delete_ordered_product()
    return redirect('orders')


def order(request):
    if isinstance(request.user, Supplier):
        return redirect('Main Page')
    ordered_products = OrderedProduct.filter_user_name(Client(request.user))
    return render(request, 'ordered_product/new_order.html', {'orders': ordered_products,
                                                              'deliveries': DeliveryLocation.objects.all,
                                                              'supplier_products': SupplierProduct.objects.all})


def add_order(request):
    if isinstance(request.user, Supplier):
        return redirect('Main Page')
    delivery = request.GET['delivery']
    supplier_product = request.GET['supplier_product']
    quantity = request.GET['quantity']
    print(delivery)
    OrderedProduct.order(DeliveryLocation.objects.get(id=int(delivery)),
                         Client.objects.get(user_name=request.user),
                         SupplierProduct.objects.get(supplier_product_id=int(supplier_product)),
                         int(quantity))
    return redirect('orders')
