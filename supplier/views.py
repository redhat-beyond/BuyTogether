from django.shortcuts import render
from supplier.models import Supplier
from django.contrib.auth.decorators import user_passes_test


def get_supplier(user):
    try:
        return Supplier.objects.get(supplier_account=user)
    except Exception:
        return False


@user_passes_test(get_supplier, login_url='Not allowed')
def suppliers_page(request):
    return render(request, 'supplier/suppliers.html')
