from django.db import migrations, transaction
from delivery_location.models import DeliveryLocation
from supplier.models import Supplier
import datetime


class Migration(migrations.Migration):
    dependencies = [
        ('delivery_location', '0001_initial'),
        ('supplier', '0002_test_data'),
    ]

    def generate_data(apps, schema_editor):
        with transaction.atomic():
            test_data = [
                ('worldMaster'),
                ('ededed'),
            ]

            for userName in test_data:
                DeliveryLocation(user_name=Supplier.objects.get(user_name=userName),
                                 location="Qiryat Shemona",
                                 date=datetime.date(2022, 12, 30)).add_delivery_location()

    operations = [
        migrations.RunPython(generate_data),
    ]
