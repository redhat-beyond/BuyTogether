import pytest
from django.template.loader import get_template
from supplier.models import Supplier
from client.models import Client
from django.contrib.auth.models import User
import json


@pytest.mark.django_db()
class TestSignupPage:
    def test_signup_template(self):
        get_template('buy_together_app/sign_up.html')

    def test_signup_get_page(self, client):
        response = client.get("/signup")
        assert response.status_code == 200

    def test_signup_supplier(self, client):
        response = client.post(
            '/signup/supplier', {'username': "testSignUp",
                                 'password': "pokemon123",
                                 'first_name': "ash",
                                 'last_name': "katchamp",
                                 'business_name': "pokemon inc"}
        )
        assert User.objects.get(username="testSignUp") in User.objects.all()
        assert response.status_code == 302
        assert response.url == "/"
        user = User.objects.get(username="testSignUp")
        sup_account = Supplier.objects.get(supplier_account=user)
        sup_account_business_name = sup_account.business_name
        assert sup_account_business_name == "pokemon inc"

    def test_bad_signup_supplier(self, client, saved_supplier0):
        response = client.post(
            '/signup/supplier', {'username': saved_supplier0.supplier_account.username,
                                 'password': saved_supplier0.supplier_account.password,
                                 'first_name': saved_supplier0.supplier_account.first_name,
                                 'last_name': saved_supplier0.supplier_account.last_name,
                                 'business_name': saved_supplier0.business_name}
        )
        # In here we are checking that form is valid but the supplier is
        # already saved in the data base
        assert "Username is taken" in response.context['message']
        assert response.status_code == 200

    def test_signup_client(self, client):
        response = client.post(
            '/signup/client', {'username': "testSignUp",
                               'password': "pokemon123",
                               'first_name': "ash",
                               'last_name': "katchamp",
                               'area': "pokemon inc"}
        )
        assert User.objects.get(username="testSignUp") in User.objects.all()
        assert response.status_code == 302
        assert response.url == "/"
        user = User.objects.get(username="testSignUp")
        client_account = Client.objects.get(client_account=user)
        client_account_area = client_account.area
        assert client_account_area == "pokemon inc"

    def test_bad_signup_client(self, client, saved_client0):
        response = client.post(
            '/signup/client', {'username': saved_client0.client_account.username,
                               'password': saved_client0.client_account.password,
                               'first_name': saved_client0.client_account.first_name,
                               'last_name': saved_client0.client_account.last_name,
                               'area': saved_client0.area}
        )
        # In here we are checking that form is valid but the client is
        # already saved in the data base
        assert "Username is taken" in response.context['message']
        assert response.status_code == 200

    def test_signup_invalid_wrong_format(self, client):
        response = client.post(
            '/signup/supplier', {'user_name': "testSignUp",
                                 'password': "pokemon123",
                                 'first_name': "ash",
                                 'last_name': "katchamp",
                                 'business_name': "pokemon inc"}
        )
        # we are checking that the form of the body of the request is
        # invalid instead of username we set it to user_name which is wrong
        error_msg = {"username": [{"message": "This field is required.", "code": "required"}]}
        assert json.dumps(error_msg) in response.context['invalid']
        assert response.status_code == 200

    def test_signup_invalid_missing_business_name(self, client):
        response = client.post(
            '/signup/supplier', {'username': "testSignUp",
                                 'password': "pokemon123",
                                 'first_name': "ash",
                                 'last_name': "katchamp",
                                 }
        )
        # we are checking that the form of the body of the request is
        # invalid instead of username we set it to user_name which is wrong
        error_msg = {"business_name": [{"message": "This field is required.", "code": "required"}]}
        assert json.dumps(error_msg) in response.context['invalid']
        assert response.status_code == 200

    def test_signup_get_supplier(self, client):
        response = client.get('/signup/supplier',)
        assert response.status_code == 200
        assert "Please sign up" in response.context['message']

    def test_signup_get_client(self, client):
        response = client.get('/signup/client',)
        assert response.status_code == 200
        assert "Please sign up" in response.context['message']
