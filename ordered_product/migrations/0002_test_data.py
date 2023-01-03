from django.db import migrations, transaction
from client.models import Client
from delivery_location.models import DeliveryLocation
from supplier_product.models import SupplierProduct
from product.models import Product
from supplier.models import Supplier
from ordered_product.models import OrderedProduct
import datetime


class Migration(migrations.Migration):
    dependencies = [
        ('ordered_product', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):

        test_data = [
                3, 4
        ]

        with transaction.atomic():
            for qn in test_data:
                sup = Supplier(user_name="bestSup",
                               first_name="Yuval",
                               last_name="Cohen",
                               password="1234",
                               business_name="bestSup")
                sup.save()

                client = Client(user_name="meitar1996",
                                first_name="Meitar",
                                last_name="Rizner",
                                password="123456",
                                area="North Israel")
                client.save()

                product = Product(qr_code="Q5o76MbdiNbXprNEnHfpcGWFp1CMF8XY",
                                  product_name="Apple",
                                  description="Sweety!")
                product.save()

                sup_product = SupplierProduct(supplier_product_id=1,
                                              qr_code=product,
                                              user_name=sup,
                                              price=10,
                                              quantity=50)
                sup_product.save()

                del_location = DeliveryLocation(user_name=sup,
                                                location="Kiryat Shmona",
                                                date=datetime.date(2022, 12, 30))
                del_location.save()

                OrderedProduct(delivery_location_id=del_location,
                               user_name=client,
                               supplier_product_id=sup_product,
                               quantity=qn).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
