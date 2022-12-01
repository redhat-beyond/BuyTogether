import pytest


@pytest.mark.django_db()
def test_member_app_entrypoint(client):
    response = client.get("/products/")
    assert response.status_code == 200
