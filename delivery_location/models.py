from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from supplier.models import Supplier


class DeliveryLocation(models.Model):
    user_name = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    location = models.CharField(max_length=32, validators=[MinLengthValidator(1)])
    date = models.DateField()

    def add_delivery_location(self):
        self.save()
        try:
            DeliveryLocation.full_clean(self)
        except ValidationError as e:
            self.delete()
            raise e
        return self

    def remove_delivery_location(self):
        DeliveryLocation.objects.get(id=self.id).delete()

    def update_date(self, newdate):
        self.date = newdate
        self.save()

    def update_location(self, new_location):
        if not new_location:
            raise ValidationError("Please put a new location with length bigger than zero")
        else:
            self.location = new_location
            self.save()

    @staticmethod
    def filter_by_supplier_and_location(supplier, specific_location):
        return DeliveryLocation.objects.filter(user_name=supplier, location=specific_location)

    @staticmethod
    def filter_by_location(supplier):
        return DeliveryLocation.objects.filter(user_name=supplier)

    @staticmethod
    def get_all_delivery_locations():
        return DeliveryLocation.objects.all()

    @staticmethod
    def get_delivery_location_by_id(a_id):
        return DeliveryLocation.objects.get(id=a_id)

    @staticmethod
    def remove_delivery_location_by_id(a_id):
        DeliveryLocation.objects.get(id=a_id).delete()
