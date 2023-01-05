import pytest
from enum import Enum
from supplier import models
from client.models import Client
from delivery_location.models import DeliveryLocation
from product.models import Product
from supplier_product.models import SupplierProduct
from ordered_product.models import OrderedProduct
import datetime


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
    models.Supplier.save_supplier(supplier0)
    return supplier0


@pytest.fixture()
def client0():
    return Client(user_name='liorsil1',
                  first_name='lior1',
                  last_name='silberman1',
                  password='1234qwer1',
                  area='Tel Aviv1')


@pytest.fixture
def saved_client0(client0):
    client0.save_client()
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
    return Product(qr_code="Q5o76MbdiNbXprNEnHfpcGWFp1CMF8XY",
                   product_name="Apple",
                   description="Sweety!")


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
def supplier_product1(product1, supplier0):
    return SupplierProduct(qr_code=product1,
                           user_name=supplier0,
                           price=5,
                           quantity=50)


@pytest.fixture
def saved_supplier_product0(supplier_product0):
    supplier_product0.save()
    return supplier_product0


@pytest.fixture
def delivery_location0(supplier0):
    return DeliveryLocation(user_name=supplier0, location="Kiryat Shemona", date=datetime.date(2022, 12, 30))


@pytest.fixture
def delivery_location1(supplier0):
    return DeliveryLocation(user_name=supplier0, location="Haifa", date=datetime.date(2022, 12, 31))


@pytest.fixture
def save_objects(delivery_location0, supplier0, supplier_product0, client0, product0):
    client0.save()
    product0.save()
    supplier0.save()
    supplier_product0.save()
    delivery_location0.save()


@pytest.fixture
def ordered_product0(delivery_location0, client0, supplier_product0):
    return OrderedProduct(
        delivery_location_id=delivery_location0,
        user_name=client0,
        supplier_product_id=supplier_product0,
        quantity=3)
