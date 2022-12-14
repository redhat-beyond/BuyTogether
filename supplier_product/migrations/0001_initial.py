import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0002_test_data'),
        ('supplier', '0002_test_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierProduct',
            fields=[
                ('supplier_product_id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('quantity', models.IntegerField()),
                ('qr_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.supplier')),
            ],
            options={
                'unique_together': {('user_name', 'qr_code')},
            },
        ),
    ]
