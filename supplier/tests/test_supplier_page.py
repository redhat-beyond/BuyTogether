import pytest
from unittest.mock import Mock, call
from django.contrib.auth.models import User
from supplier.models import Supplier
from supplier.views import action_display_all_products, get_supplier
from supplier.views import get_product_by_name_and_supplier, action_search_product, show_deliveries
from django.test import RequestFactory
from supplier import views
from supplier_product.models import SupplierProduct
from product.models import Product
from delivery_location.models import DeliveryLocation


@pytest.fixture
def searched_product_string():
    return 'searched_product'


@pytest.fixture
def get_request():
    request = RequestFactory().get('/suppliers/')
    return request


@pytest.fixture
def get_request_with_data(saved_supplier_product0,
                          searched_product_string):
    data = {searched_product_string: saved_supplier_product0.qr_code.product_name}
    request = RequestFactory().get('/suppliers/', data)
    return request


@pytest.fixture
def non_supplier_mock():
    mock = Mock()
    mock.supplier_account = User.objects.create_user(username='Asaf102',
                                                     password='litza')
    return mock


@pytest.fixture
def request_searched_product_mock():
    mock = Mock()
    mock.GET = {}
    return mock


@pytest.fixture
def render_mock(monkeypatch):
    mock = Mock()
    monkeypatch.setattr(views, views.render.__name__, mock)
    return mock


@pytest.fixture
def messages_mock(monkeypatch):
    mock = Mock()
    monkeypatch.setattr(views, "messages", mock)
    return mock


@pytest.fixture
def all_products_mock(saved_supplier0,
                      saved_supplier_product0,
                      saved_supplier_product1):
    mock = Mock()
    mock.return_value = SupplierProduct.objects.filter(user_name=saved_supplier0)
    return mock


@pytest.mark.django_db()
def test_success_entry(client, saved_supplier0):
    client.force_login(user=saved_supplier0.supplier_account)
    assert saved_supplier0 in Supplier.objects.all()
    respone = client.get('/suppliers/')
    assert respone.status_code == 200


@pytest.mark.django_db()
def test_fail_entry(client, non_supplier_mock):
    client.force_login(user=non_supplier_mock.supplier_account)
    assert non_supplier_mock not in Supplier.objects.all()
    respone = client.get('/suppliers/')
    assert respone.status_code != 200


@pytest.mark.django_db()
def test_supplier_check_false(non_supplier_mock):
    assert non_supplier_mock not in Supplier.objects.all()
    assert get_supplier(non_supplier_mock.supplier_account) is False


@pytest.mark.django_db()
def test_supplier_check_true(saved_supplier0):
    assert saved_supplier0 in Supplier.objects.all()
    assert get_supplier(saved_supplier0) == saved_supplier0


@pytest.mark.django_db()
def test_get_product_return_supplier_product(request_searched_product_mock,
                                             saved_supplier0,
                                             saved_supplier_product0,
                                             saved_supplier_product1,
                                             searched_product_string):
    assert saved_supplier_product0.user_name == saved_supplier0
    assert saved_supplier_product1.user_name == saved_supplier0
    request_searched_product_mock.GET[searched_product_string] = saved_supplier_product0.qr_code.product_name
    result = get_product_by_name_and_supplier(request_searched_product_mock, saved_supplier0)
    assert result.first() == saved_supplier_product0


@pytest.mark.django_db()
def test_get_product_sup_dont_have_product(request_searched_product_mock,
                                           saved_supplier0,
                                           saved_product0,
                                           searched_product_string):
    assert saved_product0 in Product.objects.all()
    request_searched_product_mock.GET[searched_product_string] = saved_product0.product_name
    assert get_product_by_name_and_supplier(request_searched_product_mock, saved_supplier0) is None


@pytest.mark.django_db()
def test_get_product_return_none(request_searched_product_mock,
                                 saved_supplier0,
                                 searched_product_string):

    request_searched_product_mock.GET[searched_product_string] = 'Fizzibublach'
    assert get_product_by_name_and_supplier(request_searched_product_mock, saved_supplier0) is None


@pytest.mark.django_db()
def test_searched_product_with_data(get_request_with_data,
                                    render_mock,
                                    saved_supplier_product0, saved_supplier0):

    context = show_deliveries(saved_supplier0)
    response = action_search_product(get_request_with_data, saved_supplier_product0, context)
    assert response == render_mock.return_value

    # data = {'supplier_products': saved_supplier_product0}
    context['supplier_products'] = saved_supplier_product0
    assert render_mock.call_args_list == [
        call(get_request_with_data, 'supplier/suppliers.html', context)
    ]


@pytest.mark.django_db()
def test_searched_product_without_data(get_request_with_data,
                                       render_mock,
                                       messages_mock, saved_supplier0):
    context = show_deliveries(saved_supplier0)
    response = action_search_product(get_request_with_data, None, context)
    assert response == render_mock.return_value
    messages_mock.info.assert_called_with(
        get_request_with_data, 'Product Not Found'
    )
    assert render_mock.call_args_list == [
        call(get_request_with_data, 'supplier/suppliers.html', context)
    ]


@pytest.mark.django_db()
def test_action_display_all_products(get_request,
                                     saved_supplier0,
                                     render_mock):
    context = show_deliveries(saved_supplier0)
    response = action_display_all_products(get_request, saved_supplier0, context)
    assert response == render_mock.return_value

    data = set(SupplierProduct.objects.filter(user_name=saved_supplier0))
    context['supplier_products'] = data
    assert render_mock.call_args_list == [
        call(get_request, 'supplier/suppliers.html', context)
    ]


@pytest.mark.django_db()
def test_supplier_deliveries(client, delivery_location0):
    delivery_location0.add_delivery_location()
    client.force_login(user=delivery_location0.user_name.supplier_account)
    response = client.get('/suppliers/')
    assert list(response.context['supplier_deliveries']) == [delivery_location0]


@pytest.mark.django_db()
def test_create_delivery(client, saved_supplier0):
    client.force_login(user=saved_supplier0.supplier_account)
    response = client.get('/suppliers/?location=tel+aviv&date=2023-01-18&add=Add')
    assert len(DeliveryLocation.objects.filter(user_name=saved_supplier0)) != 0
    assert response.status_code == 302
    assert client.get('/suppliers/').status_code == 200


@pytest.mark.django_db()
def test_show_deliveries_with_no_deliveries(client, saved_supplier0):
    client.force_login(user=saved_supplier0.supplier_account)
    response = client.get('/suppliers/')
    assert len(DeliveryLocation.objects.filter(user_name=saved_supplier0)) == 0
    assert response.status_code == 200
    assert len(list(response.context['supplier_deliveries'])) == 0
    assert response.context['message'] == "You don't have any deliveries yet"


@pytest.mark.django_db()
def test_remove_delivery(client, saved_supplier0):
    client.force_login(user=saved_supplier0.supplier_account)
    client.get('/suppliers/?location=tel+aviv&date=2023-01-18&add=Add')
    assert len(DeliveryLocation.objects.filter(user_name=saved_supplier0)) != 0
    response = client.get('/suppliers/?location=tel+aviv&date=2023-01-18&delete=Delete')
    assert len(DeliveryLocation.objects.filter(user_name=saved_supplier0)) == 0
    assert response.status_code == 302
    assert client.get('/suppliers/').status_code == 200
