from django.db import migrations, transaction
from supplier.models import Supplier


class Migration(migrations.Migration):
    dependencies = [
        ('supplier', '0006_rename_ssupplier_account_supplier_supplier_account'),
    ]

    def generate_data(apps, schema_editor):
        test_data = [
            ('worldMaster', 'ash', 'katchamp', 'pokemon123', 'pokemon inc'),
            ('ededed', 'edd', 'eddy', 'jawbreaker101', 'jawbreaker inc'),
        ]

        with transaction.atomic():
            for userName, firstName, lastName, passwrd, businessName in test_data:
                sup = Supplier(user_name=userName,
                               first_name=firstName,
                               last_name=lastName,
                               password=passwrd,
                               business_name=businessName)
                Supplier.save_supplier(sup)

    operations = [
        migrations.RunPython(generate_data),
    ]
