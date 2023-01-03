# Generated by Django 4.1.3 on 2023-01-05 13:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_test_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='password',
            field=models.CharField(help_text='Password',
                                   max_length=256,
                                   validators=[django.core.validators.MinLengthValidator(6)]),
        ),
    ]