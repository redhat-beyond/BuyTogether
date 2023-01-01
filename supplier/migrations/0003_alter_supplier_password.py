# Generated by Django 4.1.3 on 2023-01-05 20:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='password',
            field=models.CharField(help_text='Password',
                                   max_length=256,
                                   validators=[django.core.validators.MinLengthValidator(6)]),
        ),
    ]
