from django.contrib import admin
from supplier_product.models import SupplierProduct


class SupplierProductAdmin(admin.ModelAdmin):
    list_display = ('supplier_product_id', 'qr_code', 'user_name', 'price', 'quantity')


admin.site.register(SupplierProduct, SupplierProductAdmin)
