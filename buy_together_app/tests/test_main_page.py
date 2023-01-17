import pytest


@pytest.mark.django_db()
def test_main_page_logged_supplier(client, saved_supplier0):
    client.force_login(saved_supplier0.supplier_account)
    assert 'supplier' in client.get('/').context


@pytest.mark.django_db()
def test_main_page_not_logged_supplier(client, saved_client0):
    client.force_login(saved_client0.client_account)
    assert 'supplier' not in client.get('/').context
