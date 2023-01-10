from django.db import migrations, transaction
from product.models import Product
from supplier_product.models import SupplierProduct, Supplier
import importlib
from django.contrib.auth.models import User


initial = importlib.import_module("product.migrations.0002_test_data")
TEST_DATA = initial.TEST_DATA


class Migration(migrations.Migration):
    dependencies = [
        ('supplier_product', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        test_SUPPLIER_DATA = [
            ('rawanabu', 'rawan', 'willn', '9aa85qa5', 'rawanab99'),
        ]
        with transaction.atomic():
            for qr, name, desc in TEST_DATA:
                prod = Product(qr_code=qr, product_name=name, description=desc)
                prod.save_product()
            for userName, firstName, lastName, passwrd, businessName in test_SUPPLIER_DATA:
                sup = Supplier(supplier_account=User.objects.create_user(username=userName,
                                                                         password=passwrd,
                                                                         first_name=firstName,
                                                                         last_name=lastName,
                                                                         ),
                               business_name=businessName)
                Supplier.save_supplier(sup)
            SupplierProduct.save_sup_product(SupplierProduct(supplier_product_id=9953,
                                                             qr_code=prod, user_name=sup, price=55, quantity=63))
    operations = [
        migrations.RunPython(generate_data),
    ]
