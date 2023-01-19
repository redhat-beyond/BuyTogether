import pytest
from ordered_product.models import OrderedProduct
from client.models import Client
from supplier_product.models import SupplierProduct
from delivery_location.models import DeliveryLocation
from product.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


@pytest.fixture
def invalid_supplier_product_id():
    return '0'


@pytest.fixture
def invalid_delivery_location_id():
    return '9797'


def client_check(user):
    try:
        return Client.objects.get(client_account=user)
    except ObjectDoesNotExist:
        return False


class TestsCreateNewOrderedProduct:
    @pytest.mark.django_db()
    def test_display_new_order_page(self, client, client0_login):
        response = client.get('/ordered_product/new_order/')
        assert response.status_code == 200
        template_names = set(template.origin.template_name for template in response.templates)
        assert 'ordered_product/new_order.html' in template_names

    @pytest.mark.django_db()
    def test_get_available_products_by_valid_product_name(self, client, saved_supplier_product0, client0_login):
        VALID_PRODUCT_NAME = saved_supplier_product0.qr_code.product_name
        product = Product.objects.get(product_name=VALID_PRODUCT_NAME)
        supplier_products_by_objects_filter = list(SupplierProduct.objects.filter(qr_code=product))
        assert saved_supplier_product0 in supplier_products_by_objects_filter
        response = client.get(
            '/ordered_product/new_order/search_product_by_product_name',
            {'product_name': VALID_PRODUCT_NAME}
        )
        assert response.status_code == 200
        assert response.context['message'] == ""
        supplier_products_by_the_web_view = list(response.context['supplier_products'])
        supplier_products_by_the_web_view = sorted(
            supplier_products_by_the_web_view, key=lambda supplier_product: supplier_product.supplier_product_id
        )
        supplier_products_by_objects_filter == sorted(
            supplier_products_by_the_web_view, key=lambda supplier_product: supplier_product.supplier_product_id
        )
        assert supplier_products_by_the_web_view == supplier_products_by_objects_filter

    @pytest.mark.django_db()
    def test_get_products_by_invalid_product_name(self, client, client0_login):
        INVALID_PRODUCT_NAME = 'Eggplant'
        with pytest.raises(ObjectDoesNotExist):
            Product.objects.get(product_name=INVALID_PRODUCT_NAME)
        response = client.get(
            '/ordered_product/new_order/search_product_by_product_name',
            {'product_name': INVALID_PRODUCT_NAME}
        )
        assert response.status_code == 200
        assert response.context['message'] == "Invalid product name"
        assert list(response.context['supplier_products']) == []

    @pytest.mark.django_db()
    def test_get_unavailable_products_by_valid_product_name(self, client, saved_product1, client0_login):
        PRODUCT_NAME = saved_product1.product_name
        supplier_products = SupplierProduct.objects.filter(qr_code=saved_product1)
        assert list(supplier_products) == []
        response = client.get(
            '/ordered_product/new_order/search_product_by_product_name',
            {'product_name': PRODUCT_NAME}
        )
        assert response.status_code == 200
        assert response.context['message'] == "No products found"
        assert list(response.context['supplier_products']) == []

    @pytest.mark.django_db()
    def test_get_available_products_valid_by_client_area(
        self,
        client,
        saved_supplier_product0,
        saved_client0,
        delivery_location2,
        client0_login
    ):
        delivery_location2.add_delivery_location()
        assert delivery_location2.location == saved_client0.area
        assert delivery_location2.user_name == saved_supplier_product0.user_name

        deliveries_in_client_area = DeliveryLocation.objects.filter(location=saved_client0.area)
        assert delivery_location2 in deliveries_in_client_area
        supplier_products_by_objects_filter = []
        for delivery in deliveries_in_client_area:
            supplier_products_by_objects_filter += SupplierProduct.objects.filter(user_name=delivery.user_name)
        assert saved_supplier_product0 in supplier_products_by_objects_filter
        supplier_products_by_objects_filter = list(supplier_products_by_objects_filter)
        response = client.get('/ordered_product/new_order/search_product_by_location')
        assert response.status_code == 200
        assert response.context['message'] == ""
        supplier_products_by_the_web_view = list(response.context['supplier_products'])
        supplier_products_by_the_web_view = sorted(
            supplier_products_by_the_web_view, key=lambda supplier_product: supplier_product.supplier_product_id
        )
        supplier_products_by_objects_filter == sorted(
            supplier_products_by_the_web_view, key=lambda supplier_product: supplier_product.supplier_product_id
        )
        assert supplier_products_by_the_web_view == supplier_products_by_objects_filter

    @pytest.mark.django_db()
    def test_get_products_by_invalid_client_area(self, client, client0_login):
        INVALID_CLIENT_AREA = ''
        deliveries_in_client_area = DeliveryLocation.objects.filter(location=INVALID_CLIENT_AREA)
        assert list(deliveries_in_client_area) == []
        response = client.get('/ordered_product/new_order/search_product_by_location')
        assert response.status_code == 200
        assert response.context['message'] == "No products found in your area"
        assert response.context['supplier_products'] == []

    @pytest.mark.django_db()
    def test_get_unavailable_products_by_valid_client_area(
        self,
        client,
        saved_client0,
        delivery_location3,
        client0_login
    ):
        delivery_location3.add_delivery_location()
        assert saved_client0.area == delivery_location3.location

        deliveries_in_client_area = DeliveryLocation.objects.filter(location=saved_client0.area)
        assert delivery_location3 in deliveries_in_client_area
        supplier_products_by_objects_filter = []
        for delivery in deliveries_in_client_area:
            supplier_products_by_objects_filter += SupplierProduct.objects.filter(user_name=delivery.user_name)
        assert list(supplier_products_by_objects_filter) == []
        response = client.get('/ordered_product/new_order/search_product_by_location')
        assert response.status_code == 200
        assert response.context['message'] == "No products found"
        assert response.context['supplier_products'] == []

    @pytest.mark.django_db()
    def test_get_available_products_by_valid_supplier_user_name(
        self,
        client,
        saved_supplier_product0,
        saved_client0,
        delivery_location2,
        client0_login
    ):
        VALID_SUPPLIER_USER_NAME = saved_supplier_product0.user_name.supplier_account.username
        delivery_location2.add_delivery_location()
        assert delivery_location2.location == saved_client0.area
        assert delivery_location2.user_name == saved_supplier_product0.user_name
        supplier_products_by_objects_filter = list(SupplierProduct.objects.filter(
            user_name=saved_supplier_product0.user_name
        ))
        assert saved_supplier_product0 in supplier_products_by_objects_filter
        response = client.get(
            '/ordered_product/new_order/search_supplier_catalog_by_user_name',
            {'supplier_user_name': VALID_SUPPLIER_USER_NAME}
        )
        assert response.status_code == 200
        assert response.context['message'] == ""
        supplier_products_by_the_web_view = list(response.context['supplier_products'])
        supplier_products_by_the_web_view = sorted(
            supplier_products_by_the_web_view, key=lambda supplier_product: supplier_product.supplier_product_id
        )
        supplier_products_by_objects_filter == sorted(
            supplier_products_by_the_web_view, key=lambda supplier_product: supplier_product.supplier_product_id
        )
        assert supplier_products_by_the_web_view == supplier_products_by_objects_filter

    @pytest.mark.django_db()
    def test_get_products_by_invalid_supplier_user_name(self, client, client0_login):
        INVALID_SUPPLIER_USER_NAME = ''
        with pytest.raises(ObjectDoesNotExist):
            User.objects.get(username=INVALID_SUPPLIER_USER_NAME)
        response = client.get(
            '/ordered_product/new_order/search_supplier_catalog_by_user_name',
            {'supplier_user_name': INVALID_SUPPLIER_USER_NAME}
        )
        assert response.status_code == 200
        assert response.context['message'] == "Supplier no found"
        assert response.context['supplier_products'] == []

    @pytest.mark.django_db()
    def test_get_products_by_valid_supplier_user_name_and_no_deliveries_in_client_area(
        self,
        client,
        saved_client0,
        saved_supplier0,
        client0_login
    ):
        VALID_SUPPLIER_USER_NAME = saved_supplier0.supplier_account.username
        deliveries_of_supplier0 = DeliveryLocation.objects.filter(user_name=saved_supplier0)
        for delivery in deliveries_of_supplier0:
            assert delivery.location != saved_client0.area
        response = client.get(
            '/ordered_product/new_order/search_supplier_catalog_by_user_name',
            {'supplier_user_name': VALID_SUPPLIER_USER_NAME}
        )
        assert response.status_code == 200
        assert response.context['message'] == "No products found in your area"
        assert list(response.context['supplier_products']) == []

    @pytest.mark.django_db()
    def test_get_unavailable_products_by_valid_supplier_user_name(
        self,
        client,
        saved_supplier1,
        saved_client0,
        delivery_location3,
        client0_login
    ):
        VALID_SUPPLIER_USER_NAME = saved_supplier1.supplier_account.username
        delivery_location3.add_delivery_location()
        assert delivery_location3.location == saved_client0.area
        assert delivery_location3.user_name == saved_supplier1
        supplier_products_by_objects_filter = list(SupplierProduct.objects.filter(
            user_name=saved_supplier1
        ))
        assert supplier_products_by_objects_filter == []
        response = client.get(
            '/ordered_product/new_order/search_supplier_catalog_by_user_name',
            {'supplier_user_name': VALID_SUPPLIER_USER_NAME}
        )
        assert response.status_code == 200
        assert response.context['message'] == "No products found"
        supplier_products_by_the_web_view = list(response.context['supplier_products'])
        supplier_products_by_the_web_view = sorted(
            supplier_products_by_the_web_view, key=lambda supplier_product: supplier_product.supplier_product_id
        )
        supplier_products_by_objects_filter == sorted(
            supplier_products_by_the_web_view, key=lambda supplier_product: supplier_product.supplier_product_id
        )
        assert supplier_products_by_the_web_view == supplier_products_by_objects_filter

    @pytest.mark.django_db()
    def test_find_valid_delivery_of_valid_supplier_product(
        self,
        client,
        saved_client0,
        saved_supplier0,
        saved_supplier_product0,
        delivery_location2,
        client0_login
    ):
        delivery_location2.add_delivery_location()
        assert saved_supplier_product0.user_name == saved_supplier0
        assert delivery_location2.user_name == saved_supplier0
        assert delivery_location2.location == saved_client0.area

        response = client.get(
            f'/ordered_product/new_order/find_delivery/{saved_supplier_product0.supplier_product_id}'
        )
        assert response.status_code == 200

        template_names = set(
            template.origin.template_name for template in response.templates
        )
        assert 'ordered_product/new_order.html' in template_names

        delivery_location_by_objects_filter = DeliveryLocation.objects.filter(
            user_name=saved_supplier0, location=saved_client0.area
        )
        assert delivery_location2 in delivery_location_by_objects_filter
        assert response.context['message'] == ""
        assert response.context['sup_pro_id'] == saved_supplier_product0.supplier_product_id
        delivery_location_by_the_web_view = response.context['deliveries']
        assert list(delivery_location_by_the_web_view) == list(delivery_location_by_objects_filter)

    @pytest.mark.django_db()
    def test_find_invalid_delivery_of_valid_supplier_product(
        self,
        client,
        saved_client0,
        saved_supplier0,
        saved_supplier_product0,
        delivery_location0,
        client0_login
    ):
        delivery_location0.add_delivery_location()
        assert saved_supplier_product0.user_name == saved_supplier0
        assert delivery_location0.user_name == saved_supplier0
        assert delivery_location0.location != saved_client0.area

        response = client.get(
            f'/ordered_product/new_order/find_delivery/{saved_supplier_product0.supplier_product_id}'
        )
        assert response.status_code == 200

        template_names = set(
            template.origin.template_name for template in response.templates
        )
        assert 'ordered_product/new_order.html' in template_names

        delivery_location_by_objects_filter = DeliveryLocation.objects.filter(
            user_name=saved_supplier0, location=saved_client0.area
        )
        assert delivery_location0 not in delivery_location_by_objects_filter
        assert list(delivery_location_by_objects_filter) == []
        assert response.context['message'] == "No delivery found at '"+saved_client0.area+"'"
        assert response.context['sup_pro_id'] == saved_supplier_product0.supplier_product_id
        delivery_location_by_the_web_view = response.context['deliveries']
        assert list(delivery_location_by_the_web_view) == list(delivery_location_by_objects_filter)

    @pytest.mark.django_db()
    def test_find_delivery_of_invalid_supplier_product(self, client, invalid_supplier_product_id, client0_login):
        with pytest.raises(ObjectDoesNotExist):
            SupplierProduct.objects.get(supplier_product_id=invalid_supplier_product_id)
        response = client.get('/ordered_product/new_order/find_delivery/'+invalid_supplier_product_id)
        assert response.status_code == 302
        assert response['Location'] == '/client/'

    @pytest.mark.django_db()
    def test_valid_order_summary(
        self,
        client,
        saved_supplier_product0,
        delivery_location0,
        client0_login
    ):
        delivery_location0.add_delivery_location()
        supplier_product_by_objects_filter = SupplierProduct.objects.get(
            supplier_product_id=saved_supplier_product0.supplier_product_id
        )
        delivery_location_by_objects_filter = DeliveryLocation.objects.get(
            id=delivery_location0.id
        )

        assert saved_supplier_product0 == supplier_product_by_objects_filter
        assert delivery_location0 == delivery_location_by_objects_filter

        response = client.get(
            f'/ordered_product/new_order/order_summary/'
            f'{saved_supplier_product0.supplier_product_id},{delivery_location0.id}'
        )
        assert response.status_code == 200

        template_names = set(
            template.origin.template_name for template in response.templates
        )
        assert 'ordered_product/new_order.html' in template_names

        supplier_products_by_the_web_view = response.context['supplier_product']
        delivery_location_by_the_web_view = response.context['delivery_location']
        assert supplier_products_by_the_web_view == supplier_product_by_objects_filter
        assert delivery_location_by_the_web_view == delivery_location_by_objects_filter

    @pytest.mark.django_db()
    def test_invalid_order_summary(
        self,
        client,
        invalid_delivery_location_id,
        invalid_supplier_product_id,
        client0_login
    ):
        with pytest.raises(ObjectDoesNotExist):
            SupplierProduct.objects.get(supplier_product_id=invalid_supplier_product_id)
        with pytest.raises(ObjectDoesNotExist):
            DeliveryLocation.objects.get(id=invalid_delivery_location_id)

        response = client.get(
            f'/ordered_product/new_order/order_summary/'
            f'{invalid_supplier_product_id},{invalid_delivery_location_id}'
        )
        assert response.status_code == 302
        assert response['Location'] == '/client/'

    @pytest.mark.django_db()
    def test_valid_complete_order(
        self,
        client,
        saved_supplier_product0,
        delivery_location0,
        client0,
        client0_login
    ):
        delivery_location0.add_delivery_location()
        with pytest.raises(ObjectDoesNotExist):
            OrderedProduct.objects.get(
                delivery_location_id=delivery_location0.id,
                user_name=client0,
                supplier_product_id=saved_supplier_product0.supplier_product_id,
                quantity=5
            )

        response = client.get(
            f'/ordered_product/new_order/complete_order/'
            f'{saved_supplier_product0.supplier_product_id},{delivery_location0.id}',
            {'quantity': 5}
        )
        assert OrderedProduct.objects.get(
            delivery_location_id=delivery_location0.id,
            user_name=client0,
            supplier_product_id=saved_supplier_product0.supplier_product_id,
            quantity=5
        )
        assert response.status_code == 302
        assert response['Location'] == '/client/'
        template_names = set(template.origin.template_name for template in response.templates)
        assert template_names == set()

    @pytest.mark.django_db()
    def test_complete_order_invalid_quantity(
        self,
        client,
        saved_supplier_product0,
        delivery_location0,
        client0,
        client0_login
    ):
        invalid_quantity = 'a'
        delivery_location0.add_delivery_location()
        with pytest.raises(ValueError):
            OrderedProduct.objects.get(
                delivery_location_id=delivery_location0.id,
                user_name=client0,
                supplier_product_id=saved_supplier_product0.supplier_product_id,
                quantity=invalid_quantity
            )
        response = client.get(
            f'/ordered_product/new_order/complete_order/'
            f'{saved_supplier_product0.supplier_product_id},{delivery_location0.id}',
            {'quantity': invalid_quantity}
        )
        with pytest.raises(ValueError):
            OrderedProduct.objects.get(
                delivery_location_id=delivery_location0.id,
                user_name=client0,
                supplier_product_id=saved_supplier_product0.supplier_product_id,
                quantity=invalid_quantity
            )
        assert response.status_code == 302
        assert response['Location'] == '/client/'
        template_names = set(template.origin.template_name for template in response.templates)
        assert template_names == set()

    @pytest.mark.django_db()
    def test_complete_order_invalid_supplier_product(
        self,
        client,
        invalid_supplier_product_id,
        delivery_location0,
        client0,
        client0_login
    ):
        delivery_location0.add_delivery_location()
        with pytest.raises(ObjectDoesNotExist):
            SupplierProduct.objects.get(supplier_product_id=invalid_supplier_product_id)

        response = client.get(
            f'/ordered_product/new_order/complete_order/'
            f'{invalid_supplier_product_id},{delivery_location0.id}',
            {'quantity': 5}
        )
        assert response.status_code == 302
        assert response['Location'] == '/client/'
        template_names = set(template.origin.template_name for template in response.templates)
        assert template_names == set()

    @pytest.mark.django_db()
    def test_complete_order_invalid_delivery_location(
        self,
        client,
        saved_supplier_product0,
        invalid_delivery_location_id,
        client0,
        client0_login
    ):
        with pytest.raises(ObjectDoesNotExist):
            DeliveryLocation.objects.get(id=invalid_delivery_location_id)

        response = client.get(
            f'/ordered_product/new_order/complete_order/'
            f'{saved_supplier_product0.supplier_product_id},{invalid_delivery_location_id}',
            {'quantity': 5}
        )
        assert response.status_code == 302
        assert response['Location'] == '/client/'
        template_names = set(template.origin.template_name for template in response.templates)
        assert template_names == set()

    @pytest.mark.django_db()
    def test_pay_order(self, client, client0_login):
        response = client.get('/ordered_product/new_order/pay_order')
        template_names = set(
            template.origin.template_name for template in response.templates
        )
        assert 'ordered_product/pay_order.html' in template_names
