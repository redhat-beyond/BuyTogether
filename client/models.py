from django.db import models
from django.core.validators import MinLengthValidator
from buy_together_app.models import User


class Client(User):
    area = models.CharField(max_length=32,
                            validators=[MinLengthValidator(1)],
                            help_text="area")

    def save_client(self):
        """Saves new client 'safely'
        Args:
            client - the Client wanted to be saved.
        Returns:
            None.
        raises:
        ValidationError error: if fields input aren't valid.
        """
        Client.full_clean(self)
        self.save()

    def delete_client(self):
        """Deletes client 'safely'
        Args:
            client - the client wanted to be deleted
        Returns:
            None.
        raises:
        ValueError error: if the client is not in DB.
        """
        Client.objects.get(user_name=self.user_name).delete()
