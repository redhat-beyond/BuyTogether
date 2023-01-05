import pytest
from django.template.loader import get_template
from supplier.models import Supplier
from client.models import Client


@pytest.mark.django_db()
class TestSignupPage:
    def test_signup_template(self):
        get_template('buy_together_app/sign_up.html')

    def test_signup_supplier(self, client):
        response = client.post(
            '/signup/supplier', {'user_name': "testSignUp",
                                 'password': "pokemon123",
                                 'first_name': "ash",
                                 'last_name': "katchamp",
                                 'business_name': "pokemon inc"}
        )
        assert Supplier.objects.get(user_name="testSignUp") in list(Supplier.objects.all())
        assert response.status_code == 302
        assert response.url == "/"

    def test_bad_signup_supplier(self, client, saved_supplier0):
        response = client.post(
            '/signup/supplier', {'user_name': saved_supplier0.user_name,
                                 'password': saved_supplier0.password,
                                 'first_name': saved_supplier0.first_name,
                                 'last_name': saved_supplier0.last_name,
                                 'business_name': saved_supplier0.business_name}
        )
        assert "Username is taken" in response.context['message']

    def test_signup_client(self, client):
        response = client.post(
            '/signup/client', {'user_name': "testSignUp",
                               'password': "pokemon123",
                               'first_name': "ash",
                               'last_name': "katchamp",
                               'area': "pokemon inc"}
        )
        assert Client.objects.get(user_name="testSignUp") in list(Client.objects.all())
        assert response.status_code == 302
        assert response.url == "/"

    def test_bad_signup_client(self, client, saved_client0):
        response = client.post(
            '/signup/client', {'user_name': saved_client0.user_name,
                               'password': saved_client0.password,
                               'first_name': saved_client0.first_name,
                               'last_name': saved_client0.last_name,
                               'area': saved_client0.area}
        )
        assert "Username is taken" in response.context['message']
