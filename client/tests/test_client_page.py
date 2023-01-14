import pytest
from client.models import Client
from django.contrib.auth.models import User
from client.views import client_check
from ordered_product.models import OrderedProduct
from unittest.mock import Mock


@pytest.fixture
def non_client_mock():
    mock = Mock()
    mock.client_account = User.objects.create_user(username='Asaf102',
                                                   password='litza')
    return mock


class TestClientLogin:
    @pytest.mark.django_db()
    def test_success_entry(self, client, saved_client0):
        client.force_login(user=saved_client0.client_account)
        assert saved_client0 in Client.objects.all()
        respone = client.get('/client/')
        assert respone.status_code == 200

    @pytest.mark.django_db()
    def test_fail_entry(self, client, non_client_mock):
        client.force_login(user=non_client_mock.client_account)
        assert non_client_mock not in Client.objects.all()
        respone = client.get('/client/')
        assert respone.status_code != 200

    @pytest.mark.django_db()
    def test_client_check_false(self, non_client_mock):
        assert non_client_mock not in Client.objects.all()
        assert client_check(non_client_mock.client_account) is False

    @pytest.mark.django_db()
    def test_client_check_true(self, saved_client0):
        assert saved_client0 in Client.objects.all()
        assert client_check(saved_client0) == saved_client0


class TestOrderList:
    @pytest.mark.django_db()
    def test_orders_list_no_conatins_orders(self, client, saved_client0, client0_login):
        response = client.get('/client/')
        template_names = set(template.origin.template_name for template in response.templates)
        assert 'client/clients.html' in template_names
        clients_orders_by_the_web_view = list(response.context['orders'])
        client_orders_by_objects_filter = list(OrderedProduct.filter_user_name(saved_client0))
        assert clients_orders_by_the_web_view == []
        assert client_orders_by_objects_filter == []
        assert response.context['message'] == "No orders found"
        assert response.context['sum'] == 0

    @pytest.mark.django_db()
    def test_orders_list_conatins_orders(self, client, saved_client0, ordered_product0, client0_login):
        assert ordered_product0.user_name == saved_client0
        ordered_product0.save_ordered_product()
        response = client.get('/client/')
        template_names = set(template.origin.template_name for template in response.templates)
        assert 'client/clients.html' in template_names
        client_orders_by_the_web_view = list(response.context['orders'])
        client_orders_by_objects_filter = list(OrderedProduct.filter_user_name(saved_client0))
        assert ordered_product0 in client_orders_by_objects_filter
        assert client_orders_by_the_web_view == client_orders_by_objects_filter
        assert response.context['message'] == ""
        assert response.context['sum'] == ordered_product0.total_price()
