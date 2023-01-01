import pytest
from client.models import Client
from django.core.exceptions import ObjectDoesNotExist, ValidationError


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
    def test_delete_not_exist_clinet(self, client0):
        assert client0 not in Client.objects.all()
        with pytest.raises(ObjectDoesNotExist):
            client0.delete_client()

    @pytest.mark.django_db()
    def test_fail_to_add_client_user_name(self, client0):
        short_user_name = 'lior'
        client0.user_name = short_user_name
        with pytest.raises(ValidationError):
            client0.save_client()

    @pytest.mark.django_db()
    def test_fail_to_add_client_first_name(self, client0):
        empty_field = ''
        client0.first_name = empty_field
        with pytest.raises(ValidationError):
            client0.save_client()

    @pytest.mark.django_db()
    def test_fail_to_add_client_last_name(self, client0):
        empty_field = ''
        client0.last_name = empty_field
        with pytest.raises(ValidationError):
            client0.save_client()

    @pytest.mark.django_db()
    def test_fail_to_add_client_password(self, client0):
        short_password = '123'
        client0.password = short_password
        with pytest.raises(ValidationError):
            client0.save_client()

    @pytest.mark.django_db()
    def test_fail_to_add_client_area(self, client0):
        empty_field = ''
        client0.area = empty_field
        with pytest.raises(ValidationError):
            client0.save_client()
