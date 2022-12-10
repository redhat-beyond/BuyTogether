from django.db import migrations, transaction
from supplier.models import Supplier


class Migration(migrations.Migration):
    dependencies = [
        ('supplier', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        test_data = [
            ('worldMaster', 'ash', 'katchamp', 'pokemon123', 'supplier', 'pokemon inc'),
            ('ed', 'edd', 'eddy', 'jawbreaker101', 'supplier', 'jawbreaker inc'),
        ]

        with transaction.atomic():
            for userName, firstName, lastName, passwrd, userType, businessName in test_data:
                Supplier(user_name=userName,
                         first_name=firstName,
                         last_name=lastName,
                         password=passwrd,
                         user_type=userType,
                         business_name=businessName).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
