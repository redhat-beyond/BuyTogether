import pytest
from conftest import Fields, TestFields
from django.core.exceptions import FieldDoesNotExist, ValidationError
from supplier.models import Supplier


class TestSupplierModel:
    @pytest.mark.django_db()
    def test_save_supplier(self, supplier0):
        """Test - checks if supplier is saved in DB.

        Args:
            supplier0: fixture from module conftest.py.

        Returns:
            None.
        """
        Supplier.save_supplier(supplier0)
        assert supplier0 in Supplier.objects.all()

    @pytest.mark.django_db()
    def test_delete_supplier(self, saved_supplier0):
        """Test - checks if supplier is not in DB after deletion.

        Args:
            saved_supplier0: fixture from module conftest.py.

        Returns:
            None.
        """
        Supplier.delete_supplier(saved_supplier0)
        assert saved_supplier0 not in Supplier.objects.all()

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
        for attri, testAttri in zip(Fields, TestFields):
            assert saved_supplier0 in Supplier.filter_by_field(attri.name,
                                                               testAttri.value)

    @pytest.mark.django_db()
    def test_get_all_suppliers(self):
        """Test - checks if All suppliers are found in the DB.

        Args:
            None.

        Returns:
            None.
        """
        for sup in Supplier.get_all_suppliers():
            assert sup in Supplier.objects.all()

    @pytest.mark.django_db()
    def test_field_does_not_exits(self):
        """Test - checks if non existing field can be looked in DB.

        Args:
            None.

        Returns:
            None.
        """
        with pytest.raises(FieldDoesNotExist):
            Supplier.filter_by_field('Life', 'Programmer')

    @pytest.mark.django_db()
    def test_fail_to_add_supplier(self, supplier0):
        """Test - checks for adding non valid supplier

        Trying to save supplier with unvalid fields.

        Args:
            None.
        Returns:
            None.
        """
        with pytest.raises(ValidationError):
            supplier0.user_name = ''
            Supplier.save_supplier(supplier0)
