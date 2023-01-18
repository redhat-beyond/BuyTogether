import pytest


@pytest.mark.django_db()
class TestSignupPage:
    def test_log_out(self, client, saved_supplier0):
        client.force_login(user=saved_supplier0.supplier_account)
        response = client.get('/logout')
        assert response.status_code == 302
        assert response['Location'] == '/'
        assert response.wsgi_request.user.is_authenticated is False
