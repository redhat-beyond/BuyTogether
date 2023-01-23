from django.shortcuts import redirect
from supplier_product.models import SupplierProduct
from django.template.exceptions import TemplateDoesNotExist
from django.http import HttpResponse
from django.db.models import F


def increase_quantity(request, id, n):
    SupplierProduct.objects.filter(supplier_product_id=id).update(quantity=F('quantity')+n)
    try:
        product = SupplierProduct.objects.get(supplier_product_id=id)
    except SupplierProduct.DoesNotExist:
        raise HttpResponse("Product does not exist")
    context = {'product': product}
    try:
        return redirect(request.META.get('HTTP_REFERER', '/'), context)
    except TemplateDoesNotExist:
        return HttpResponse("Template not found")


def decrease_quantity(request, id, n):
    try:
        product = SupplierProduct.objects.get(supplier_product_id=id)
    except SupplierProduct.DoesNotExist:
        raise HttpResponse("Product does not exist")
    context = {'product': product}
    if product.quantity > n:
        SupplierProduct.objects.filter(supplier_product_id=id).update(quantity=F('quantity')-n)
    else:
        try:
            context = {'product': product}
            return redirect(request.META.get('HTTP_REFERER', '/'), context)
        except TemplateDoesNotExist:
            return HttpResponse("Template not found")
    try:
        context = {'product': product}
        return redirect(request.META.get('HTTP_REFERER', '/'), context)
    except TemplateDoesNotExist:
        return HttpResponse("Template not found")
