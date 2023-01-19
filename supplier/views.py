from django.shortcuts import render
from supplier.models import Supplier
from delivery_location.models import DeliveryLocation
from django.contrib.auth.decorators import user_passes_test
from supplier_product.models import SupplierProduct
from product.models import Product
from django.contrib import messages
from django.shortcuts import redirect


def get_supplier(user):
    try:
        return Supplier.objects.get(supplier_account=user)
    except Exception:
        return False


def get_product_by_name_and_supplier(request, supplier):
    prod_name = request.GET['searched_product']
    if prod_name:
        product = Product.filter_name(prod_name).first()
        supplier_product = SupplierProduct.objects.filter(qr_code=product,
                                                          user_name=supplier)
        if supplier_product.exists():
            return supplier_product
    return None


def action_search_product(request, supplier_product, context):
    if supplier_product:
        context['supplier_products'] = supplier_product
        return render(request, 'supplier/suppliers.html', context)
    else:
        messages.info(request, 'Product Not Found')
        return render(request, 'supplier/suppliers.html', context)


def action_display_all_products(request, supplier, context):
    data = set(SupplierProduct.objects.filter(user_name=supplier))
    context['supplier_products'] = data
    return render(request, 'supplier/suppliers.html', context)


@user_passes_test(get_supplier, login_url='Not allowed')
def suppliers_page(request):
    supplier = get_supplier(request.user)
    context = show_deliveries(supplier)

    if 'add' in request.GET:
        location = request.GET['location'].capitalize()
        date = request.GET['date']
        create_delivery(supplier, location, date)
        return redirect('/suppliers/')

    if 'delete' in request.GET:
        location = request.GET['location']
        date = request.GET['date']
        remove_delivery(supplier, location, date)
        return redirect('/suppliers/')

    if 'searched_product' in request.GET:
        return action_search_product(request, get_product_by_name_and_supplier(request, supplier), context)

    return action_display_all_products(request, supplier, context)


def show_deliveries(supplier):
    supplier_deliveries = DeliveryLocation.objects.filter(user_name=supplier)
    message = ''
    if len(supplier_deliveries) == 0:
        message = "You don't have any deliveries yet"
    return {'message': message, 'supplier_deliveries': supplier_deliveries}


def create_delivery(supplier, location, date):
    delivery = DeliveryLocation.objects.filter(user_name=supplier, location__icontains=location, date=date).first()
    if delivery is not None:
        return

    DeliveryLocation(user_name=supplier, location=location, date=date).add_delivery_location()


def remove_delivery(supplier, location, date):
    delivery = DeliveryLocation.objects.filter(user_name=supplier, location__icontains=location, date=date).first()
    if delivery is not None:
        delivery.remove_delivery_location()
