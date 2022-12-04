import pytest
from product.models import Product
from django.core.exceptions import ValidationError

QR = "W5P76MbdiNbXprNEnHfpcGWFp1CMF8XY"
NAME = "Banana"
DESCRIPTION = "Good!"
TEST_DATA = [
            ('Q5o76MbdiNbXprNEnHfpcGWFp1CMF8XY', 'Apple', 'Sweety!'),
            ('Q5o76MbdiNbXprNEnHfpcGWFp1CMF8ad', 'Banana', "Good!"),
        ]


@pytest.fixture
def product0():
    return Product(qr_code=QR, product_name=NAME, description=DESCRIPTION)


@pytest.fixture
def saved_product0(product0):
    product0.save_product()
    return product0


class TestProductModel:
    @pytest.mark.django_db()
    def test_save_delete_product(self, saved_product0):
        temp = Product(saved_product0.qr_code, saved_product0.product_name, saved_product0.description)
        assert saved_product0 in Product.objects.all()
        saved_product0.delete_product()
        assert saved_product0 not in Product.objects.all()
        temp.save()
        assert temp in Product.objects.all()

    @pytest.mark.django_db()
    def test_delete_non_existing_product(self):
        test_doesnotexist = Product("DOESNOTEXIST", "TEST", "TEST")
        with pytest.raises(Product.DoesNotExist):
            test_doesnotexist.delete_product()

    @pytest.mark.django_db()
    def test_filter_by_qr(self, saved_product0):
        assert None is Product.filter_qr("")
        assert [saved_product0] == list(Product.filter_qr(saved_product0.qr_code))

    @pytest.mark.django_db()
    def test_filter_by_product_name(self, saved_product0):
        assert saved_product0 in list(Product.filter_name(saved_product0.product_name))
        assert saved_product0 not in list(Product.filter_name(""))

    @pytest.mark.django_db()
    def test_filter_by_description(self, saved_product0):
        assert saved_product0 in Product.filter_description(saved_product0.description)
        assert saved_product0 not in Product.filter_description("")

    @pytest.mark.django_db()
    def test_get_all_products(self):
        """
            Suppose we have empty database and we need to add to it 3 apples
            we need to check if the all products are actually apples and same
            with same qr_codes
        """
        prods = [Product(*td) for td in TEST_DATA]
        for p in prods:
            Product.save_product(p)
        assert list(Product.get_all_products()) == prods

    @pytest.mark.django_db()
    def test_validators(self):
        try:
            temp1 = Product(qr_code="123", product_name="1", description="1")
            temp2 = Product(qr_code="AQ5o76MbdiNbXprNEnHfpcGWFp1CMF8X", product_name="", description="1")
            temp3 = Product(qr_code="AQ5o76MbdiNbXprNEnHfpcGWFp1CMF8X", product_name="2", description="")
            Product.save_product(temp1)
            Product.save_product(temp2)
            Product.save_product(temp3)
        except ValidationError:
            assert temp1 not in Product.objects.all()
            assert temp2 not in Product.objects.all()
            assert temp3 not in Product.objects.all()
