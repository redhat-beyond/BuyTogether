from django.db import migrations, transaction
from delivery_location.models import DeliveryLocation
from supplier.models import Supplier
import datetime


class Migration(migrations.Migration):
    dependencies = [
        ('delivery_location', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        with transaction.atomic():
            test_data = [
                ('worldMaster', 'ash', 'katchamp', 'pokemon123', 'pokemon inc'),
                ('ed', 'edd', 'eddy', 'jawbreaker101', 'jawbreaker inc'),
            ]

            for userName, firstName, lastName, passwrd, businessName in test_data:
                sup = Supplier(
                    user_name=userName,
                    first_name=firstName,
                    last_name=lastName,
                    password=passwrd,
                    business_name=businessName
                                )
                sup.save()
                DeliveryLocation(user_name=sup, location="Qiryat Shemona", date=datetime.date(2022, 12, 30)).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
