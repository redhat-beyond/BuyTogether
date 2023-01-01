from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import FieldDoesNotExist
from buy_together_app.models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class Supplier(CustomUser):
    """Supplier class inherit from User abstract class.

    Supplier class lets the app user to do variety of actions
    which evolves the Product and Delivery class.

    Attributes:
        business_name: a string which holds the Supplier business name.
    """
    supplier_account = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
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
        # The Supplier object will be deleted automatically once the User object it references is deleted.
        User.objects.get(username=supplier.user_name).delete()

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
        supplier.password = make_password(salt="Random", password=supplier.password)
        User.objects.create_user(username=supplier.user_name,
                                 password=supplier.password)
        supplier.supplier_account = User.objects.get(username=supplier.user_name)
        Supplier.full_clean(supplier)
        supplier.save()
