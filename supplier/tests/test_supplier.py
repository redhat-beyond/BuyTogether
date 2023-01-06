import pytest
from conftest import Fields, TestFields
from django.core.exceptions import FieldDoesNotExist, ValidationError, ObjectDoesNotExist
from supplier.models import Supplier
from django.contrib.auth.hashers import make_password


class TestSupplierModel:
    @pytest.mark.django_db()
    def test_save_supplier(self, supplier0):
        assert supplier0 not in Supplier.objects.all()
        Supplier.save_supplier(supplier0)
        assert supplier0 in Supplier.objects.all()

    @pytest.mark.django_db()
    def test_delete_not_existed_supplier(self, supplier0):
        with pytest.raises(ObjectDoesNotExist):
            assert supplier0 not in Supplier.objects.all()
            Supplier.delete_supplier(supplier0)

    @pytest.mark.django_db()
    def test_delete_exist_supplier(self, supplier0):
        assert supplier0 not in Supplier.objects.all()
        Supplier.save_supplier(supplier0)
        assert supplier0 in Supplier.objects.all()
        Supplier.delete_supplier(supplier0)
        assert supplier0 not in Supplier.objects.all()

    @pytest.mark.django_db()
    def test_fail_to_save_supplier(self, supplier0):
        with pytest.raises(ValidationError):
            supplier0.user_name = '123'
            Supplier.save_supplier(supplier0)

    @pytest.mark.django_db()
    def test_filter_by_field(self, saved_supplier0):
        """Test - checks the Supplier method filter by field.

        The test checks whether the fixtured Supplier - saved_supplier0 -
        can be found in the returned query set of each attribute and
        attribute value given to the method "filter by field".

        Args:
            saved_supplier0: fixture from module conftest.py.

        Returns:
            None.
        """
        supplier_fields = [field.name for field in Supplier._meta.get_fields()]
        for attri, testAttri in zip(Fields, TestFields):
            assert attri.name in supplier_fields
            if (attri.name == "password"):
                assert saved_supplier0 in Supplier.filter_by_field(attri.name,
                                                                   make_password(salt="Random",
                                                                                 password=testAttri.value))
            else:
                assert saved_supplier0 in Supplier.filter_by_field(attri.name,
                                                                   testAttri.value)

    @pytest.mark.django_db()
    def test_non_exists_field_value(self, saved_supplier0):
        assert saved_supplier0 in Supplier.objects.all()
        Supplier.delete_supplier(saved_supplier0)
        assert saved_supplier0 not in Supplier.filter_by_field(Fields.user_name.name,
                                                               TestFields.USER_NAME_TEST.value)

    @pytest.mark.django_db()
    def test_field_does_not_exits(self):
        with pytest.raises(FieldDoesNotExist):
            Supplier.filter_by_field('Life', 'Programmer')
