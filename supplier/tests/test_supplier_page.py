import pytest
from unittest.mock import Mock
from django.contrib.auth.models import User
from supplier.models import Supplier
from supplier.views import get_supplier


@pytest.fixture
def non_supplier_mock():
    mock = Mock()
    mock.supplier_account = User.objects.create_user(username='Asaf102',
                                                     password='litza')
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
