import pytest
from delivery_location.models import DeliveryLocation
from django.core.exceptions import ValidationError
import datetime


class TestDeliveryLocationModel:
    @pytest.mark.django_db()
    def test_add_delivery_location(self, delivery_location0):
        delivery_location0.add_delivery_location()
        assert delivery_location0 in DeliveryLocation.objects.all()

    @pytest.mark.django_db()
    def test_delete_non_existing_delivery_location(self):
        with pytest.raises(DeliveryLocation.DoesNotExist):
            DeliveryLocation.remove_delivery_location_by_id(-1)

    @pytest.mark.django_db()
    def test_delete_delivery_location(self, delivery_location0):
        delivery_location0.add_delivery_location()
        assert delivery_location0 in DeliveryLocation.objects.all()
        delivery_location0.remove_delivery_location()
        assert delivery_location0 not in DeliveryLocation.objects.all()

    @pytest.mark.django_db()
    def test_filter_by_id(self, delivery_location0):
        delivery_location0.add_delivery_location()
        assert delivery_location0 == DeliveryLocation.get_delivery_location_by_id(delivery_location0.id)

    @pytest.mark.django_db()
    def test_filter_by_id_that_does_not_exist(self):
        with pytest.raises(DeliveryLocation.DoesNotExist):
            DeliveryLocation.get_delivery_location_by_id(-1)

    @pytest.mark.django_db()
    def test_filter_by_location_from_supplier(self, delivery_location0):
        delivery_location0.add_delivery_location()
        assert delivery_location0 in list(
            DeliveryLocation.filter_by_supplier_and_location(delivery_location0.user_name, "Kiryat Shemona"))

    @pytest.mark.django_db()
    def test_filter_by_location_that_does_not_exist_from_supplier(self, saved_supplier0):
        assert [] == list(DeliveryLocation.filter_by_supplier_and_location(saved_supplier0,
                                                                           "LOCATION THAT IS NOT RELATED TO SUPPLIER0"))

    @pytest.mark.django_db()
    def test_filter_by_location(self, delivery_location0, delivery_location1):
        delivery_location0.add_delivery_location()
        delivery_location1.add_delivery_location()
        delivery_location0.update_location("Haifa")
        delivery_location1.update_location("Haifa")
        assert set([delivery_location0, delivery_location1]) == set(list(
            DeliveryLocation.filter_by_location(delivery_location0.location)))

    @pytest.mark.django_db()
    def test_filter_by_location_that_does_not_exist(self):
        assert [] == list(DeliveryLocation.filter_by_location("NOT EXISTED LOCATION"))

    @pytest.mark.django_db()
    def test_update_delivery_location_date(self, delivery_location0):
        delivery_location0.add_delivery_location()
        testnewdate = datetime.date(2023, 1, 1)
        delivery_location0.update_date(testnewdate)
        assert testnewdate == delivery_location0.date

    @pytest.mark.django_db()
    def test_update_delivery_location_location(self, delivery_location0):
        delivery_location0.add_delivery_location()
        delivery_location0.update_location("Yafo")
        assert "Yafo" == delivery_location0.location

    @pytest.mark.django_db()
    def test_validators(self, saved_supplier0):
        valtest = DeliveryLocation(user_name=saved_supplier0, location="", date=datetime.date(2022, 12, 31))
        with pytest.raises(ValidationError):
            valtest.add_delivery_location()
