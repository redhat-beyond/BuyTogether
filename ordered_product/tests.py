import pytest
from ordered_product.models import OrderedProduct
from django.core.exceptions import ValidationError


@pytest.fixture
def save_objects(delivery_location0, supplier0, supplier_product0, client0, product0):
    client0.save()
    product0.save()
    supplier0.save()
    supplier_product0.save()
    delivery_location0.save()


class TestOrderedProductModel():
    @pytest.mark.django_db()
    def test_save_and_delete_ordered_product(self, ordered_product0, save_objects):
        assert ordered_product0 not in OrderedProduct.objects.all()
        ordered_product0.save_ordered_product()
        assert ordered_product0 in OrderedProduct.objects.all()
        ordered_product0.delete_ordered_product()
        assert ordered_product0 not in OrderedProduct.objects.all()

    @pytest.mark.django_db()
    def test_filter_by_user_name(self, ordered_product0, save_objects, client1, client0):
        ordered_product0.user_name = client0
        ordered_product0.save_ordered_product()
        assert ordered_product0 not in list(OrderedProduct.filter_user_name(client1))
        assert ordered_product0 in list(OrderedProduct.filter_user_name(client0))

    @pytest.mark.django_db()
    def test_filter_by_supplier_product_id(self, ordered_product0, supplier_product0, supplier_product1, save_objects):
        ordered_product0.supplier_product_id = supplier_product0
        ordered_product0.save_ordered_product()
        assert ordered_product0 not in list(OrderedProduct.filter_supplier_product_id(supplier_product1))
        assert ordered_product0 in list(OrderedProduct.filter_supplier_product_id(supplier_product0))

    @pytest.mark.django_db()
    def test_filter_delivery_location_id(self, ordered_product0, delivery_location0, delivery_location1, save_objects):
        ordered_product0.delivery_location_id = delivery_location0
        ordered_product0.save_ordered_product()
        assert ordered_product0 not in list(OrderedProduct.filter_delivery_location_id(delivery_location1))
        assert ordered_product0 in list(OrderedProduct.filter_delivery_location_id(delivery_location0))

    @pytest.mark.django_db()
    def test_validators(self, delivery_location0, client0, supplier_product0, save_objects):
        temp_ordered_product = OrderedProduct(
                delivery_location_id=delivery_location0,
                user_name=client0,
                supplier_product_id=supplier_product0,
                quantity=-2)
        with pytest.raises(ValidationError):
            temp_ordered_product.save_ordered_product()
        assert temp_ordered_product not in OrderedProduct.objects.all()

    @pytest.mark.django_db()
    def test_decrease_quantity(self, ordered_product0, save_objects):
        ordered_product0.quantity = 3
        ordered_product0.save_ordered_product()
        ordered_product0.decrease_quantity(1)
        assert ordered_product0.quantity == 2
        assert ordered_product0 in OrderedProduct.objects.all()
        ordered_product0.decrease_quantity(8)
        assert ordered_product0.quantity < 0
        assert ordered_product0 not in OrderedProduct.objects.all()

    @pytest.mark.django_db()
    def test_increase_quantity(self, ordered_product0, save_objects):
        ordered_product0.quantity = 3
        ordered_product0.save_ordered_product()
        ordered_product0.increase_quantity(6)
        assert ordered_product0.quantity == 9
        assert ordered_product0 in OrderedProduct.objects.all()

    @pytest.mark.django_db()
    def test_order(self, client0, delivery_location0, supplier_product0, save_objects):
        ordered_product = OrderedProduct.order(delivery_location0, client0, supplier_product0, 8)
        assert ordered_product in OrderedProduct.objects.all()

    @pytest.mark.django_db()
    def test_invalid_order(self, client0, delivery_location0, supplier_product0, save_objects):
        with pytest.raises(ValidationError):
            OrderedProduct.order(delivery_location0, client0, supplier_product0, -1)
