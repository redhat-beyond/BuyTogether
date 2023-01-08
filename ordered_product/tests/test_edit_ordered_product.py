import pytest
from ordered_product.models import OrderedProduct
from client.models import Client
from django.core.exceptions import ObjectDoesNotExist


def client_check(user):
    try:
        return Client.objects.get(client_account=user)
    except ObjectDoesNotExist:
        return False


class TestsEditOrderedProduct:
    @pytest.mark.django_db()
    def test_change_valid_positive_quantity_to_valid_order(
        self,
        client,
        saved_client0,
        ordered_product0,
        client0_login
    ):
        positive_quantity = 5
        ordered_product0.save_ordered_product()
        assert ordered_product0.user_name == saved_client0
        quantity_before_change = OrderedProduct.objects.get(id=ordered_product0.id).quantity
        response = client.get(f'/ordered_product/orders/{ordered_product0.id}', {'quantity': positive_quantity})
        quantity_after_change = OrderedProduct.objects.get(id=ordered_product0.id).quantity
        assert quantity_after_change == quantity_before_change+positive_quantity
        assert response.status_code == 302
        assert response['Location'] == '/client/'
        template_names = set(template.origin.template_name for template in response.templates)
        assert template_names == set()

    @pytest.mark.django_db()
    def test_change_valid_negative_quantity_to_valid_order(
        self,
        client,
        saved_client0,
        ordered_product0,
        client0_login
    ):
        negative_quantity = -1
        ordered_product0.save_ordered_product()
        assert ordered_product0.quantity > 1
        assert ordered_product0.user_name == saved_client0
        quantity_before_change = OrderedProduct.objects.get(id=ordered_product0.id).quantity
        response = client.get(f'/ordered_product/orders/{ordered_product0.id}', {'quantity': negative_quantity})
        assert ordered_product0 in OrderedProduct.objects.all()
        quantity_after_change = OrderedProduct.objects.get(id=ordered_product0.id).quantity
        assert quantity_after_change == quantity_before_change+negative_quantity
        assert response.status_code == 302
        assert response['Location'] == '/client/'
        template_names = set(template.origin.template_name for template in response.templates)
        assert template_names == set()

    @pytest.mark.django_db()
    def test_change_valid_zeroed_quantity_to_valid_order(self, client, saved_client0, ordered_product0, client0_login):
        quantity = 0
        ordered_product0.save_ordered_product()
        assert ordered_product0.user_name == saved_client0
        quantity_before_change = OrderedProduct.objects.get(id=ordered_product0.id).quantity
        response = client.get(f'/ordered_product/orders/{ordered_product0.id}', {'quantity': quantity})
        quantity_after_change = OrderedProduct.objects.get(id=ordered_product0.id).quantity
        assert quantity_after_change == quantity_before_change
        assert response.status_code == 302
        assert response['Location'] == '/client/'
        template_names = set(template.origin.template_name for template in response.templates)
        assert template_names == set()

    @pytest.mark.django_db()
    def test_change_invalid_quantity_to_valid_order(self, client, ordered_product0, client0_login):
        ordered_product0.save_ordered_product()
        invalid_quantity = 'a'
        quantity_before_change = OrderedProduct.objects.get(id=ordered_product0.id).quantity
        response = client.get(f'/ordered_product/orders/{ordered_product0.id}', {'quantity': invalid_quantity})
        quantity_after_change = OrderedProduct.objects.get(id=ordered_product0.id).quantity
        assert quantity_before_change == quantity_after_change
        assert response.status_code == 302
        assert response['Location'] == '/client/'
        template_names = set(template.origin.template_name for template in response.templates)
        assert template_names == set()

    @pytest.mark.django_db()
    def test_change_valid_quantity_to_invalid_order(self, client, client0_login):
        invalid_order_product_id = 'a'
        with pytest.raises(ValueError):
            OrderedProduct.objects.get(id=invalid_order_product_id)
        response = client.get(f'/ordered_product/orders/{invalid_order_product_id}', {'quantity': 5})
        assert response.status_code == 404

    @pytest.mark.django_db()
    def test_delete_valid_order(self, client, saved_client0, ordered_product0, client0_login):
        assert ordered_product0.user_name == saved_client0
        ordered_product0.save_ordered_product()
        assert ordered_product0 in OrderedProduct.objects.filter(user_name=saved_client0)
        response = client.get(f'/ordered_product/orders/{ordered_product0.id},delete')
        assert ordered_product0 not in OrderedProduct.objects.filter(user_name=saved_client0)
        assert response.status_code == 302
        assert response['Location'] == '/client/'
        template_names = set(template.origin.template_name for template in response.templates)
        assert template_names == set()

    @pytest.mark.django_db()
    def test_delete_invalid_order(self, client, client0_login):
        invalid_order_product_id = 'a'
        with pytest.raises(ValueError):
            OrderedProduct.objects.get(id=invalid_order_product_id)
        response = client.get(f'/ordered_product/orders/{invalid_order_product_id},delete')
        assert response.status_code == 404
