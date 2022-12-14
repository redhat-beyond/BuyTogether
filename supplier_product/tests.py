import pytest
from supplier_product.models import SupplierProduct


@pytest.mark.django_db()
class TestSupProduct:

    def test_save_supplier_product(self, supplier_product0):
        assert supplier_product0 not in SupplierProduct.objects.all()
        SupplierProduct.save_sup_product(supplier_product0)
        assert supplier_product0 in SupplierProduct.objects.all()

    def test_delete_supplier_product(self, supplier_product0):
        assert supplier_product0 not in SupplierProduct.objects.all()
        SupplierProduct.save_sup_product(supplier_product0)
        assert supplier_product0 in SupplierProduct.objects.all()
        supplier_product0.delete()
        assert supplier_product0 not in SupplierProduct.objects.all()

    def test_increase_sup_product_quantity(self, supplier_product0):
        new_quantity = supplier_product0.quantity + 1
        old_quantity = supplier_product0.quantity
        supplier_product0.increase_sup_product_quantity(new_quantity)
        assert supplier_product0.quantity == old_quantity + new_quantity

    def test_decrease_sup_product_quantity(self, supplier_product0):
        new_quantity = supplier_product0.quantity - 1
        old_quantity = supplier_product0.quantity
        supplier_product0.decrease_sup_product_quantity(new_quantity)
        assert supplier_product0.quantity == old_quantity - new_quantity

    def test_decrease_supp_product_quantiy_delete_raise_negatvie_value_exception(self, supplier_product0):
        new_quantity = -5
        with pytest.raises(ValueError):
            supplier_product0.decrease_sup_product_quantity(new_quantity)

    def test_decrease_supp_product_quantiy_delete_raise_value_error_exception(self, supplier_product0):
        new_quantity = supplier_product0.quantity + 1
        with pytest.raises(ValueError):
            supplier_product0.decrease_sup_product_quantity(new_quantity)
