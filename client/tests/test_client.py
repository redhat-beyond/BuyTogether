import pytest
from client.models import Client
from django.core.exceptions import ValidationError


class TestClientModel:
    @pytest.mark.django_db()
    def test_save_client(self, client0):
        assert client0 not in Client.objects.all()
        client0.save_client()
        assert client0 in Client.objects.all()

    @pytest.mark.django_db()
    def test_delete_client(self, saved_client0):
        assert saved_client0 in Client.objects.all()
        saved_client0.delete_client()
        assert saved_client0 not in Client.objects.all()

    @pytest.mark.django_db()
    def test_delete_not_exist_clinet(self, saved_client0):
        assert saved_client0 in Client.objects.all()
        saved_client0.delete_client()
        assert saved_client0 not in Client.objects.all()
        with pytest.raises(Exception):
            saved_client0.delete_client()

    @pytest.mark.django_db()
    def test_fail_to_add_client_area(self, client0):
        empty_field = ''
        client0.area = empty_field
        with pytest.raises(ValidationError):
            client0.save_client()
