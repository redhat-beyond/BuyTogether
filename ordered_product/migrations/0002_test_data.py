from django.db import migrations, transaction
from client.models import Client
from delivery_location.models import DeliveryLocation
from supplier_product.models import SupplierProduct
from product.models import Product
from supplier.models import Supplier
from ordered_product.models import OrderedProduct
import datetime
from django.contrib.auth.models import User


class Migration(migrations.Migration):
    dependencies = [
        ('ordered_product', '0002_initial'),
    ]

    def generate_data(apps, schema_editor):

        test_data = [
                [3, "bestSup1", "bestSup2", 1000], [4, "bestSup3", "bestSup4", 1001]
        ]

        with transaction.atomic():
            for qn, sup_usr, cli_usr, sup_prd_id in test_data:
                usr = User.objects.create_user(username=sup_usr,
                                               first_name="Yuval",
                                               last_name="Cohen",
                                               password="HaloHalo2",
                                               )
                sup = Supplier(supplier_account=usr,
                               business_name="bestSup")
                Supplier.save_supplier(sup)

                client = Client(client_account=User.objects.create_user(username=cli_usr,
                                first_name="Meitar",
                                last_name="Rizner",
                                password="123456",),
                                area="North Israel")
                client.save_client()

                product = Product.objects.get(qr_code="Q5o76MbdiNbXprNEnHfpcGWFp1CMF8XY")

                sup_product = SupplierProduct(supplier_product_id=sup_prd_id,
                                              qr_code=product,
                                              user_name=sup,
                                              price=10,
                                              quantity=50)
                SupplierProduct.save_sup_product(sup_product)

                del_location = DeliveryLocation(user_name=sup,
                                                location="Kiryat Shmona",
                                                date=datetime.date(2022, 12, 30))
                del_location.add_delivery_location()

                OrderedProduct(delivery_location_id=del_location,
                               user_name=client,
                               supplier_product_id=sup_product,
                               quantity=qn).save_ordered_product()

    operations = [
        migrations.RunPython(generate_data),
    ]
