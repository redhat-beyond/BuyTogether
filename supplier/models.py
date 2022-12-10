from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist


class User(models.Model):
    """An abstract class which holds basic user data:

    Attributes:
        user_name: a string which holds the user name, Also PK.
        first_name: a string which holds the user first name.
        last_name: a string which holds the user last name.
        password: a string which holds the user password.
    """

    user_name = models.CharField(max_length=32,
                                 primary_key=True,
                                 null=False,
                                 validators=[MinLengthValidator(6)],
                                 help_text="User Name")
    first_name = models.CharField(max_length=32,
                                  validators=[MinLengthValidator(1)],
                                  help_text="First Name")
    last_name = models.CharField(max_length=32,
                                 validators=[MinLengthValidator(1)],
                                 help_text="Last Name")
    password = models.CharField(max_length=16,
                                validators=[MinLengthValidator(6)],
                                null=False,
                                help_text="Password")

    class Meta:
        abstract = True


class Supplier(User):
    """Supplier class inherit from User abstract class.

    Supplier class lets the app user to do variety of actions
    which evolves the Product and Delivery class.

    Attributes:
        business_name: a string which holds the Supplier business name.
    """
    business_name = models.CharField(max_length=32,
                                     validators=[MinLengthValidator(6)],
                                     null=False,
                                     help_text="Business Name")

    @staticmethod
    def filter_by_field(field, field_value):
        """Fetches list of Suppliers filtered with given field and given value.

        Args:
        field:
            Supplier attribute.
        field_value:
            value which will filter the suppliers.

        Returns:
            returns a queryset containing the objects that match the specified filter conditions.

        Raises:
        FieldDoesNotExist error: if Supplier doesn't have the specified attribute.
        """
        if hasattr(Supplier, str(field)):
            return Supplier.objects.filter(**{field: field_value})
        raise FieldDoesNotExist

    @staticmethod
    def delete_supplier(supplier):
        """Deletes supplier 'safely'

        Args:
            supplier - the Supplier wanted to be deleted

        Returns:
            None.

        raises:
        ObjectDoesNotExists error: if the supplier is not in DB.
        """
        if supplier not in Supplier.objects.all():
            raise ObjectDoesNotExist
        supplier.delete()

    @staticmethod
    def save_supplier(supplier):
        """Saves new supplier 'safely'

        Args:
            supplier - the Supplier wanted to be saved.

        Returns:
            None.

        raises:
        ValidationError error: if fields input aren't valid.
        """
        Supplier.full_clean(supplier)
        supplier.save()
