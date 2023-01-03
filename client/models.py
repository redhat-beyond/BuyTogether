from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class Client(models.Model):
    client_account = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
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
        User.objects.create_user(username=self.user_name,
                                 password=self.password)
        self.client_account = User.objects.get(username=self.user_name)
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
        User.objects.get(username=self.client_account.username).delete()
