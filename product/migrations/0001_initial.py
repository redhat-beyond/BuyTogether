import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('qr_code', models.CharField(max_length=32, primary_key=True, serialize=False,
                                             validators=[django.core.validators.MinLengthValidator(32)])),
                ('product_name', models.CharField(max_length=32,
                                                  validators=[django.core.validators.MinLengthValidator(1)])),
                ('description', models.TextField(validators=[django.core.validators.MinLengthValidator(1)])),
            ],
        ),
    ]
