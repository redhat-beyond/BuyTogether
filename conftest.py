import pytest
from enum import Enum
from supplier import models
from client.models import Client


class TestFields(Enum):
    USER_NAME_TEST = 'ScrappyKoko'
    FIRST_NAME_TEST = 'Zohan'
    LAST_NAME_TEST = 'Dvir'
    PASSWORD_TEST = 'silkysmooth'
    BUSINESS_NAME_TEST = 'hair_salon_inc'


TestFields.__test__ = False


class Fields(Enum):
    user_name = 1
    first_name = 2
    last_name = 3
    password = 4
    business_name = 5


@pytest.fixture
def supplier0():
    """Creates supplier fixture.

    Creates supplier fixture for further testing.

    Args:
        None.

    Returns:
        Supplier fixture.
    """
    return models.Supplier(user_name=TestFields['USER_NAME_TEST'].value,
                           first_name=TestFields['FIRST_NAME_TEST'].value,
                           last_name=TestFields['LAST_NAME_TEST'].value,
                           password=TestFields['PASSWORD_TEST'].value,
                           business_name=TestFields['BUSINESS_NAME_TEST'].value)


@pytest.fixture
def saved_supplier0(supplier0):
    """Saves the supplier fixture.

    Args:
        Supplier0: supplier fixture.

    Returns:
        Supplier fixture.
    """
    supplier0.save()
    return supplier0


@pytest.fixture()
def client0():
    return Client(user_name='liorsil',
                  first_name='lior',
                  last_name='silberman',
                  password='1234qwer',
                  area='Tel Aviv')


@pytest.fixture
def saved_client0(client0):
    client0.save()
    return client0
