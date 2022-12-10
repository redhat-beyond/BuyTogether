import pytest
from conftest import Fields, TestFields
from supplier import models


class TestSupplierModel:
    @pytest.mark.django_db()
    def test_save_supplier(self, saved_supplier0):
        """Test - checks if supplier is saved in DB.

        Args:
            saved_supplier0: fixture from module conftest.py.

        Returns:
            None.
        """
        assert saved_supplier0 in models.Supplier.objects.all()

    @pytest.mark.django_db()
    def test_delete_supplier(self, saved_supplier0):
        """Test - checks if supplier is not in DB after deletion.

        Args:
            saved_supplier0: fixture from module conftest.py.

        Returns:
            None.
        """
        saved_supplier0.delete()
        assert saved_supplier0 not in models.Supplier.objects.all()

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
            assert saved_supplier0 in models.Supplier.filter_by_field(attri.name,
                                                                      testAttri.value)
        assert True

    @pytest.mark.django_db()
    def test_get_all_suppliers(self):
        """Test - checks if All suppliers are found in the DB.

        Args:
            None.

        Returns:
            None.
        """
        for sup in models.Supplier.get_all_suppliers():
            assert sup in models.Supplier.objects.all()
        assert True
