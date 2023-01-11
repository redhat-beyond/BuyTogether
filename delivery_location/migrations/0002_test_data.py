from django.db import migrations, transaction
from delivery_location.models import DeliveryLocation
from supplier.models import Supplier
import datetime
from django.contrib.auth.models import User


class Migration(migrations.Migration):
    dependencies = [
        ('delivery_location', '0002_initial'),
    ]

    def generate_data(apps, schema_editor):
        with transaction.atomic():
            test_data = [
                ('worldMaster'),
                ('ededed'),
            ]

            for userName in test_data:
                usr = User.objects.get(username=userName)
                sup = Supplier.objects.get(supplier_account=usr)
                DeliveryLocation(user_name=sup,
                                 location="Qiryat Shemona",
                                 date=datetime.date(2022, 12, 30)).add_delivery_location()

    operations = [
        migrations.RunPython(generate_data),
    ]
