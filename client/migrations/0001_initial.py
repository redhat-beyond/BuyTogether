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
                ('user_name', models.CharField(help_text='User Name',
                                               max_length=32,
                                               primary_key=True,
                                               serialize=False,
                                               validators=[django.core.validators.MinLengthValidator(1)])),
                ('first_name', models.CharField(help_text='First Name',
                                                max_length=32,
                                                null=True)),
                ('last_name', models.CharField(help_text='Last Name',
                                               max_length=32,
                                               null=True)),
                ('password', models.CharField(help_text='Password',
                                              max_length=16,
                                              validators=[django.core.validators.MinLengthValidator(1)])),
                ('area', models.CharField(max_length=32, validators=[django.core.validators.MinLengthValidator(1)])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
