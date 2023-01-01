from django.db import migrations, transaction
from client.models import Client


class Migration(migrations.Migration):
    dependencies = [
        ('client', '0006_rename_cclient_account_client_client_account'),
    ]

    def generate_data(apps, schema_editor):
        test_data = [
            ('liorsil', 'lior', 'silber', '1234qwer!', 'Yuvalim'),
            ('ididid', 'ido', 'silber', 'qwer1234!', 'Beit Yannai'),
        ]

        with transaction.atomic():
            for userName, firstName, lastName, passwrd, area in test_data:
                Client(user_name=userName,
                       first_name=firstName,
                       last_name=lastName,
                       password=passwrd,
                       area=area).save_client()

    operations = [
        migrations.RunPython(generate_data),
    ]
