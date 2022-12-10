import pytest
from enum import Enum
from supplier import models


class TestFields(Enum):
    USER_NAME_TEST = 'ScrappyKoko'
    FIRST_NAME_TEST = 'Zohan'
    LAST_NAME_TEST = 'Dvir'
    PASSWORD_TEST = 'silkysmooth'
    USER_TYPE_TEST = 'supplier'
    BUSINESS_NAME_TEST = 'hair_salon_inc'


class Fields(Enum):
    user_name = 1
    first_name = 2
    last_name = 3
    password = 4
    user_type = 5
    business_name = 6


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
                           user_type=TestFields['USER_TYPE_TEST'].value,
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
