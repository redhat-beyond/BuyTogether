import pytest
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from supplier.models import Supplier
from django.contrib.auth.hashers import make_password


class TestSupplierModel:
    @pytest.mark.django_db()
    def test_save_supplier(self, saved_supplier0):
        assert saved_supplier0 in Supplier.objects.all()

    @pytest.mark.django_db()
    def test_delete_not_existed_supplier(self, saved_supplier0):
        with pytest.raises(ObjectDoesNotExist):
            assert saved_supplier0 in Supplier.objects.all()
            Supplier.delete_supplier(saved_supplier0)
            assert saved_supplier0 not in Supplier.objects.all()
            Supplier.delete_supplier(saved_supplier0)

    @pytest.mark.django_db()
    def test_delete_exist_supplier(self, saved_supplier0):
        assert saved_supplier0 in Supplier.objects.all()
        Supplier.delete_supplier(saved_supplier0)
        assert saved_supplier0 not in Supplier.objects.all()

    @pytest.mark.django_db()
    def test_fail_to_save_supplier(self, supplier0):
        with pytest.raises(ValidationError):
            supplier0.business_name = ''
            Supplier.save_supplier(supplier0)
