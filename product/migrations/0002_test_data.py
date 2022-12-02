from django.db import migrations, transaction
from product.models import Product
from product.tests.File_for_tests_and_migrations import TEST_DATA


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        with transaction.atomic():
            for qr, name, desc in TEST_DATA:
                Product(qr_code=qr, product_name=name, description=desc).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
