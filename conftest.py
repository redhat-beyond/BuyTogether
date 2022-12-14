import pytest
from enum import Enum
from supplier import models
from client.models import Client
from delivery_location.models import DeliveryLocation
from product.models import Product
import datetime
from supplier_product.models import SupplierProduct


class TestFields(Enum):
    USER_NAME_TEST = 'ScrappyKoko'
    FIRST_NAME_TEST = 'Zohan'
    LAST_NAME_TEST = 'Dvir'
    PASSWORD_TEST = 'silkysmooth'
    BUSINESS_NAME_TEST = 'hair_salon_inc'


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


@pytest.fixture
def client1():
    return Client(user_name="meitar1996",
                  first_name="Meitar",
                  last_name="rizner",
                  password="1234",
                  area="Yuval")


@pytest.fixture
def product0():
    return Product(qr_code="W5P76MbdiNbXprNEnHfpcGWFp1CMF8XY",
                   product_name="Banana",
                   description="Good!")


@pytest.fixture
def product1():
    return Product(qr_code="Q5o76MbdiNbXprNEnHfpcGWFp1CMF8XZ",
                   product_name="Tomato",
                   description="Sweety!")


@pytest.fixture
def saved_product0(product0):
    product0.save_product()
    return product0


@pytest.fixture
def delivery_location0(supplier0):
    return DeliveryLocation(user_name=supplier0, location="Kiryat Shemona", date=datetime.date(2022, 12, 30))


@pytest.fixture
def delivery_location1(supplier0):
    return DeliveryLocation(user_name=supplier0, location="Haifa", date=datetime.date(2022, 12, 31))


@pytest.fixture
def supplier_product0(saved_product0, saved_supplier0):
    SUPPLIER_PRODUCT_ID = 123685
    QUANTITY = 9
    PRICE = 14
    return SupplierProduct(
        supplier_product_id=SUPPLIER_PRODUCT_ID,
        qr_code=saved_product0,
        user_name=saved_supplier0,
        price=PRICE,
        quantity=QUANTITY
    )


@pytest.fixture
def saved_supplier_product0(supplier_product0):
    supplier_product0.save()
    return supplier_product0
