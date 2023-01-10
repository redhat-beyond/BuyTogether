from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


class Supplier(models.Model):
    """Supplier class inherit from User abstract class.

    Supplier class lets the app user to do variety of actions
    which evolves the Product and Delivery class.

    Attributes:
        business_name: a string which holds the Supplier business name.
    """
    supplier_account = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    business_name = models.CharField(max_length=32,
                                     validators=[MinLengthValidator(6)],
                                     null=False,
                                     help_text="Business Name")

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
        User.objects.get(username=supplier.supplier_account.username).delete()

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
