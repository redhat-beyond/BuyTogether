from django.db import models
from django.core.validators import MinValueValidator
from product.models import Product
from supplier.models import Supplier


class SupplierProduct(models.Model):
    supplier_product_id = models.AutoField(primary_key=True)
    qr_code = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_name = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(1)])
    quantity = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ('user_name', 'qr_code')

    @staticmethod
    def save_sup_product(sup_prod):
        SupplierProduct.full_clean(sup_prod)
        sup_prod.save()

    def increase_sup_product_quantity(self, quantity):
        self.quantity += quantity
        self.save()

    def decrease_sup_product_quantity(self, quantity):
        if self.quantity < quantity:
            raise ValueError("Invalid value")
        if (quantity < 0):
            raise ValueError("Negative value")
        else:
            self.quantity -= quantity
            self.save()
