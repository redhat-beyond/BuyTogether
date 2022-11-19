from django.db import migrations, transaction
from buy_together_app.models import Product


class Migration(migrations.Migration):
    dependencies = [
        ('buy_together_app', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        TEST_DATA = [
            ('Q5o76MbdiNbXprNEnHfpcGWFp1CMF8XY', 'Apple', 'Sweety!'),
            ('Q5o76MbdiNbXprNEnHfpcGWFp1CMF8ad', 'Banana', "Good!"),
        ]
        with transaction.atomic():
            for qr, name, desc in TEST_DATA:
                Product(qr_code=qr, product_name=name, description=desc).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
