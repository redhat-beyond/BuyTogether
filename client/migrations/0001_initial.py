import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('user_name', models.CharField(max_length=32, primary_key=True, serialize=False,
                                               validators=[django.core.validators.MinLengthValidator(6)])),
                ('first_name', models.CharField(max_length=32,
                                                validators=[django.core.validators.MinLengthValidator(1)])),
                ('last_name', models.CharField(max_length=32,
                                               validators=[django.core.validators.MinLengthValidator(1)])),
                ('password', models.CharField(max_length=16,
                                              validators=[django.core.validators.MinLengthValidator(6)])),
                ('user_type', models.CharField(choices=[('Client', 'Client'), ('Supplier', 'Supplier')],
                                               max_length=16,
                                               validators=[django.core.validators.MinLengthValidator(6)])),
                ('area', models.CharField(max_length=32, validators=[django.core.validators.MinLengthValidator(6)])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
