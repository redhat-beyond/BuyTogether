from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from client.models import Client
from delivery_location.models import DeliveryLocation
from supplier_product.models import SupplierProduct


class OrderedProduct(models.Model):
    delivery_location_id = models.ForeignKey(DeliveryLocation, on_delete=models.CASCADE)
    user_name = models.ForeignKey(Client, on_delete=models.CASCADE)
    supplier_product_id = models.ForeignKey(SupplierProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    @staticmethod
    def filter_user_name(user_name):
        return OrderedProduct.objects.filter(user_name=user_name) if user_name else []

    @staticmethod
    def filter_delivery_location_id(dl_id):
        return OrderedProduct.objects.filter(delivery_location_id=dl_id) if dl_id else []

    @staticmethod
    def filter_supplier_product_id(sp_id):
        return OrderedProduct.objects.filter(supplier_product_id=sp_id) if sp_id else []

    def save_ordered_product(self):
        self.save()
        try:
            OrderedProduct.full_clean(self)
        except ValidationError as e:
            self.delete()
            raise e
        return self

    def delete_ordered_product(self):
        OrderedProduct.objects.get(id=self.id).delete()

    def decrease_quantity(self, qn):
        self.quantity -= qn
        self.save()
        if (self.quantity <= 0):
            self.delete_ordered_product()

    def increase_quantity(self, qn):
        self.quantity += qn
        self.save_ordered_product()

    @staticmethod
    def order(delivery, client, supplier_product, qn):
        if (qn <= 0):
            raise ValidationError("Quantity can't be <= 0")
        else:
            ordered_product = OrderedProduct.objects.create(delivery_location_id=delivery, user_name=client,
                                                            supplier_product_id=supplier_product, quantity=qn)
            return ordered_product.save_ordered_product()

    def total_price(self):
        return self.quantity*self.supplier_product_id.price
