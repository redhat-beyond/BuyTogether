from django.shortcuts import render
from supplier.models import Supplier
from django.contrib.auth.decorators import user_passes_test
from supplier_product.models import SupplierProduct
from product.models import Product
from django.contrib import messages


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


def action_search_product(request, supplier_product):
    if supplier_product:
        return render(request, 'supplier/suppliers.html', {'supplier_products': supplier_product})
    else:
        messages.info(request, 'Product Not Found')
        return render(request, 'supplier/suppliers.html')


def action_display_all_products(request, supplier):
    data = set(SupplierProduct.objects.filter(user_name=supplier))
    return render(request, 'supplier/suppliers.html', {'supplier_products': data})


@user_passes_test(get_supplier, login_url='Not allowed')
def suppliers_page(request):
    supplier = get_supplier(request.user)
    if 'searched_product' in request.GET:
        return action_search_product(request, get_product_by_name_and_supplier(request, supplier))

    return action_display_all_products(request, supplier)
