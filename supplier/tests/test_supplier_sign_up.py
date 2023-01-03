import pytest
from django.template.loader import get_template
from supplier.models import Supplier


@pytest.mark.django_db()
class TestSignupPage:
    def test_signup_template(self):
        get_template('supplier/supplier_sign_up.html')

    def test_signup_entry_point(self, client):
        response = client.get('/supplier/signup')
        assert response.status_code == 200

    def test_signup_user(self, client):
        response = client.post(
            '/supplier/signup', {'user_name': "testSignUp",
                                 'password': "pokemon123",
                                 'first_name': "ash",
                                 'last_name': "katchamp",
                                 'business_name': "pokemon inc"}
        )
        assert Supplier.objects.get(user_name="testSignUp") in list(Supplier.objects.all())
        assert response.status_code == 302
        assert response.url == "/"

    def test_bad_signup_user(self, client, saved_supplier0):
        response = client.post(
            '/supplier/signup', {'user_name': saved_supplier0.user_name,
                                 'password': saved_supplier0.password,
                                 'first_name': saved_supplier0.first_name,
                                 'last_name': saved_supplier0.last_name,
                                 'business_name': saved_supplier0.business_name}
        )
        assert "User name is taken" in response.context['message']
