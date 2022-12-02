from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError


class Product(models.Model):
    qr_code = models.CharField(max_length=32, validators=[MinLengthValidator(32)], primary_key=True)
    product_name = models.CharField(max_length=32, validators=[MinLengthValidator(1)])
    description = models.TextField(validators=[MinLengthValidator(1)])

    @staticmethod
    def filter_qr(qr):
        return Product.objects.filter(qr_code=qr) if qr else None

    @staticmethod
    def filter_name(nm):
        return Product.objects.filter(product_name=nm) if nm else []

    @staticmethod
    def filter_description(desc):
        return Product.objects.filter(description=desc) if desc else []

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    def save_product(self):
        self.save()
        try:
            Product.full_clean(self)
        except ValidationError as e:
            self.delete_product(self.qr_code)
            raise e
        return self

    @staticmethod
    def delete_product(prd_qr):
        try:
            prod = Product.objects.get(qr_code=prd_qr)
            prod.delete()
        except Product.DoesNotExist as e:
            raise e
        return True
