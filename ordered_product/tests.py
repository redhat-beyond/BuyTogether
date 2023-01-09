import pytest
from ordered_product.models import OrderedProduct
from django.core.exceptions import ValidationError


class TestOrderedProductModel():
    @pytest.mark.django_db()
    def test_save_and_delete_ordered_product(self, ordered_product0):
        assert ordered_product0 not in OrderedProduct.objects.all()
        ordered_product0.save_ordered_product()
        assert ordered_product0 in OrderedProduct.objects.all()
        ordered_product0.delete_ordered_product()
        assert ordered_product0 not in OrderedProduct.objects.all()

    @pytest.mark.django_db()
    def test_filter_by_user_name(self, ordered_product0, saved_client0, saved_client1):
        ordered_product0.user_name = saved_client0
        ordered_product0.save_ordered_product()
        assert ordered_product0 not in list(OrderedProduct.filter_user_name(saved_client1))
        assert ordered_product0 in list(OrderedProduct.filter_user_name(saved_client0))

    @pytest.mark.django_db()
    def test_filter_by_supplier_product_id(self, ordered_product0, saved_supplier_product1):
        ordered_product0.supplier_product_id = saved_supplier_product1
        ordered_product0.save_ordered_product()
        assert ordered_product0 in list(OrderedProduct.filter_supplier_product_id(saved_supplier_product1))

    @pytest.mark.django_db()
    def test_filter_delivery_location_id(self, ordered_product0, delivery_location1):
        delivery_location1.add_delivery_location()
        ordered_product0.delivery_location_id = delivery_location1
        ordered_product0.save_ordered_product()
        assert ordered_product0 in list(OrderedProduct.filter_delivery_location_id(delivery_location1))

    @pytest.mark.django_db()
    def test_validators(self, ordered_product0):
        ordered_product0.quantity = -2
        with pytest.raises(ValidationError):
            ordered_product0.save_ordered_product()
        assert ordered_product0 not in OrderedProduct.objects.all()

    @pytest.mark.django_db()
    def test_decrease_quantity(self, ordered_product0):
        ordered_product0.quantity = 3
        ordered_product0.save_ordered_product()
        ordered_product0.decrease_quantity(1)
        assert ordered_product0.quantity == 2
        assert ordered_product0 in OrderedProduct.objects.all()
        ordered_product0.decrease_quantity(8)
        assert ordered_product0.quantity < 0
        assert ordered_product0 not in OrderedProduct.objects.all()

    @pytest.mark.django_db()
    def test_increase_quantity(self, ordered_product0):
        ordered_product0.quantity = 3
        ordered_product0.save_ordered_product()
        ordered_product0.increase_quantity(6)
        assert ordered_product0.quantity == 9
        assert ordered_product0 in OrderedProduct.objects.all()

    @pytest.mark.django_db()
    def test_order(self, ordered_product0):
        ordered_product = OrderedProduct.order(ordered_product0.delivery_location_id,
                                               ordered_product0.user_name,
                                               ordered_product0.supplier_product_id,
                                               8)
        assert ordered_product in OrderedProduct.objects.all()

    @pytest.mark.django_db()
    def test_invalid_order(self, ordered_product0):
        with pytest.raises(ValidationError):
            OrderedProduct.order(ordered_product0.delivery_location_id,
                                 ordered_product0.user_name,
                                 ordered_product0.supplier_product_id,
                                 -1)
