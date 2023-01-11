from django.db import migrations, transaction
from product.models import Product


TEST_DATA = [
            ('Q5o76MbdiNbXprNEnHfpcGWFp1CMF8XY', 'Apple', 'Sweety!'),
            ('Q5o76MbdiNbXprNEnHfpcGWFp1CMF8ad', 'Banana', "Good!"),
        ]


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        with transaction.atomic():
            for qr, name, desc in TEST_DATA:
                Product(qr_code=qr, product_name=name, description=desc).save_product()

    operations = [
        migrations.RunPython(generate_data),
    ]
