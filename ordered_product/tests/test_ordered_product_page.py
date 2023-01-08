import pytest


class Test_order_list:
    @pytest.mark.django_db()
    def test_orders_list(self, client):
        response = client.get('/ordered_product/orders')
        assert response.status_code == 200
        template_names = set(template.origin.template_name for template in response.templates)
        assert 'ordered_product/orders.html' in template_names

    @pytest.mark.django_db()
    def test_new_order(self, client):
        response = client.get('/ordered_product/new_order')
        assert response.status_code == 200
        template_names = set(template.origin.template_name for template in response.templates)
        assert 'ordered_product/new_order.html' in template_names
