from django.shortcuts import render
from supplier.models import Supplier
from django.core.exceptions import ObjectDoesNotExist


def suppliers_page(request):
    try:
        # Will authenticate whether the user is supplier
        Supplier.objects.get(supplier_account=request.user)
        # Line 11 will be used instead line 9.
        # supplier = Supplier.objects.get(supplier_account=request.user)
    except ObjectDoesNotExist:
        return render(request, 'buy_together_app/not_allowed.html')
    return render(request, 'supplier/suppliers.html')
