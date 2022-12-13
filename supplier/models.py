from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist, ValidationError


class User(models.Model):
    """An abstract class which holds basic user data:

    Attributes:
        user_name: a string which holds the user name, Also PK.
        first_name: a string which holds the user first name.
        last_name: a string which holds the user last name.
        password: a string which holds the user password.
        user_type: a string which holds the user type, either Supplier or Client.
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
    user_type = models.CharField(max_length=16,
                                 validators=[MinLengthValidator(6)],
                                 null=False,
                                 choices=[('client', 'client'), ('supplier', 'supplier')],
                                 help_text="User Type - supplier/client")

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
    def get_all_suppliers():
        """Fetches list of all Suppliers.

        Args:
            None.

        Returns:
            returns a queryset containing all the Suppliers.
        """
        return Supplier.objects.all()

    @staticmethod
    def get_all_fields():
        """Fetches list of all Supplier fields.

        Args:
            None.

        Returns:
            returns a list of all Supplier fields.
        """
        return ['user_name', 'first_name', 'last_name',
                'password', 'user_type', 'business_name']

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
        if supplier not in Supplier.get_all_suppliers():
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
        try:
            Supplier.full_clean(supplier)
            supplier.save()
        except ValidationError as error:
            raise error
