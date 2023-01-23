from django.test import Client
from django.urls import reverse
from .models import SupplierProduct
import pytest


@pytest.mark.django_db()
def test_increase_quantity(saved_supplier_product0):
    supplier_product = saved_supplier_product0
    client = Client()
    n = 3
    response = client.get(
        reverse('supplier_product:increase_quantity', kwargs={'id': supplier_product.supplier_product_id, 'n': n}))
    updated_product = SupplierProduct.objects.get(supplier_product_id=supplier_product.supplier_product_id)
    assert updated_product.quantity == supplier_product.quantity + n
    assert response.status_code == 302


@pytest.mark.django_db()
def test_decrease_quantity(saved_supplier_product0):
    supplier_product = saved_supplier_product0
    client = Client()
    n = 3
    response = client.get(
        reverse('supplier_product:decrease_quantity', kwargs={'id': supplier_product.supplier_product_id, 'n': n}))
    updated_product = SupplierProduct.objects.get(supplier_product_id=supplier_product.supplier_product_id)
    assert updated_product.quantity == supplier_product.quantity - n
    assert response.status_code == 302
