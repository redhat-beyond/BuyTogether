from django.db import models
from django.core.validators import MinLengthValidator


class CustomUser(models.Model):
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
                                  null=False,
                                  validators=[MinLengthValidator(1)],
                                  help_text="First Name")
    last_name = models.CharField(max_length=32,
                                 null=False,
                                 validators=[MinLengthValidator(1)],
                                 help_text="Last Name")
    password = models.CharField(max_length=256,
                                validators=[MinLengthValidator(6)],
                                null=False,
                                help_text="Password")

    class Meta:
        abstract = True
