from django.db import models
from django.core.validators import MinLengthValidator


class User(models.Model):
    user_name = models.CharField(max_length=32, validators=[MinLengthValidator(6)], primary_key=True, null=False)
    first_name = models.CharField(max_length=32, validators=[MinLengthValidator(1)])
    last_name = models.CharField(max_length=32, validators=[MinLengthValidator(1)])
    password = models.CharField(max_length=16, validators=[MinLengthValidator(6)])
    user_type = models.CharField(max_length=16, validators=[MinLengthValidator(6)],
                                 choices=[('Client', 'Client'), ('Supplier', 'Supplier')])

    class Meta:
        abstract = True


class Client(User):
    area = models.CharField(max_length=32, validators=[MinLengthValidator(6)])
